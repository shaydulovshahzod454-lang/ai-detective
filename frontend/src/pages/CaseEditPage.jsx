import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  getCaseForEdit, updateCase, togglePublish,
  getCollaborators, addCollaborator, removeCollaborator,
} from '../api/myCases';
import './CaseEditPage.css';
import SceneManager from '../components/SceneManager';
import CharacterManager from '../components/CharacterManager';

// Sodda "debounce" — foydalanuvchi yozishni to'xtatgandan 1 soniya keyin saqlaydi,
// har bir harf uchun alohida so'rov yubormaslik uchun
function useDebouncedSave(value, saveFn, delay = 1000) {
  useEffect(() => {
    const timer = setTimeout(() => {
      saveFn(value);
    }, delay);
    return () => clearTimeout(timer); // oldingi timer bekor qilinadi, agar foydalanuvchi yana yozsa
  }, [value]);
}

function CaseEditPage() {
  const { caseId } = useParams();
  const navigate = useNavigate();

  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saveStatus, setSaveStatus] = useState(''); // '', 'saving', 'saved'

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [solution, setSolution] = useState('');

  const [collaborators, setCollaborators] = useState([]);
  const [newUsername, setNewUsername] = useState('');
  const [collabError, setCollabError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const data = await getCaseForEdit(caseId);
        setCaseData(data);
        setTitle(data.title);
        setDescription(data.description);
        setSolution(data.solution);

        const collabData = await getCollaborators(caseId);
        setCollaborators(collabData);
      } catch (err) {
        console.error(err);
        navigate('/my-cases'); // ruxsat yo'q yoki topilmadi — orqaga qaytaramiz
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [caseId]);

  // Har bir maydon o'zgarganda, 1 soniyadan keyin avtomatik saqlanadi
  async function autoSave(fields) {
    setSaveStatus('saving');
    try {
      await updateCase(caseId, fields);
      setSaveStatus('saved');
    } catch (err) {
      console.error(err);
      setSaveStatus('');
    }
  }

  useDebouncedSave(title, (val) => {
    if (!loading) autoSave({ title: val });
  });
  useDebouncedSave(description, (val) => {
    if (!loading) autoSave({ description: val });
  });
  useDebouncedSave(solution, (val) => {
    if (!loading) autoSave({ solution: val });
  });

  async function handleTogglePublish() {
    try {
      const updated = await togglePublish(caseId);
      setCaseData(updated);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleAddCollaborator(e) {
    e.preventDefault();
    setCollabError('');
    try {
      const newCollab = await addCollaborator(caseId, newUsername);
      setCollaborators((prev) => [...prev, newCollab]);
      setNewUsername('');
    } catch (err) {
      setCollabError(err.response?.data?.error || "Xatolik yuz berdi.");
    }
  }

  async function handleRemoveCollaborator(collabId) {
    try {
      await removeCollaborator(caseId, collabId);
      setCollaborators((prev) => prev.filter((c) => c.id !== collabId));
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) return <div className="status-message">Yuklanmoqda...</div>;

  return (
    <div className="case-edit-page">
      <Link to="/my-cases" className="back-link">← Case'larim</Link>

      <div className="edit-header">
        <h1>{caseData.title || 'Nomsiz case'}</h1>
        <span className="save-status">
          {saveStatus === 'saving' && 'Saqlanmoqda...'}
          {saveStatus === 'saved' && '✓ Saqlandi'}
        </span>
      </div>

      <button
        className={`publish-button ${caseData.is_active ? 'unpublish' : 'publish'}`}
        onClick={handleTogglePublish}
      >
        {caseData.is_active ? 'Qoralamaga o\'tkazish' : '🚀 Nashr qilish (o\'yinda ko\'rinadi)'}
      </button>

      <section className="edit-section">
        <label>Sarlavha</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} />

        <label>Tavsif (o'yinchiga ko'rinadi)</label>
        <textarea rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />

        <label>Yechim (MAXFIY)</label>
        <textarea rows={3} value={solution} onChange={(e) => setSolution(e.target.value)} />
      </section>

      <section className="edit-section">
        <h2>Hamkorlar</h2>
        <p className="section-hint">
          Bu yerga qo'shilgan foydalanuvchilar shu case'ni siz bilan birga tahrirlashi mumkin.
        </p>

        <form className="collab-form" onSubmit={handleAddCollaborator}>
          <input
            type="text"
            placeholder="Username"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
            required
          />
          <button type="submit">Qo'shish</button>
        </form>
        {collabError && <p className="form-error">{collabError}</p>}

        <div className="collab-list">
          {collaborators.map((c) => (
            <div key={c.id} className="collab-item">
              <span>{c.username}</span>
              <button onClick={() => handleRemoveCollaborator(c.id)}>✕</button>
            </div>
          ))}
          {collaborators.length === 0 && <p className="empty-hint-small">Hali hamkor yo'q</p>}
        </div>
      </section>

      <section className="edit-section">
        <h2>Scene va personajlar</h2>
        <p className="section-hint">Bu qism keyingi bosqichda qo'shiladi.</p>
      </section>
      <section className="edit-section">
        <h2>Joylar (Scene'lar)</h2>
        <SceneManager caseId={caseId} />
      </section>

      <section className="edit-section">
        <h2>Personajlar</h2>
        <CharacterManager caseId={caseId} />
      </section>
    </div>
  );
}

export default CaseEditPage;