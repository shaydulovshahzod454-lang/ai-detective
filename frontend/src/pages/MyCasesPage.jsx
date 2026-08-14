import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMyCases, createCase } from '../api/myCases';
import './MyCasesPage.css';

function MyCasesPage() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [solution, setSolution] = useState('');
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    loadCases();
  }, []);

  async function loadCases() {
    try {
      const data = await getMyCases();
      setCases(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    setError('');
    setCreating(true);

    try {
      const newCase = await createCase(title, description, solution);
      setCases((prev) => [...prev, newCase]);
      setTitle('');
      setDescription('');
      setSolution('');
      setShowForm(false);
    } catch (err) {
      console.error(err);
      setError("Case yaratishda xatolik yuz berdi.");
    } finally {
      setCreating(false);
    }
  }

  if (loading) return <div className="status-message">Yuklanmoqda...</div>;

  return (
    <div className="my-cases-page">
      <div className="my-cases-header">
        <h1>Mening case'larim</h1>
        <button className="new-case-button" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Bekor qilish' : '+ Yangi case'}
        </button>
      </div>

      {showForm && (
        <form className="new-case-form" onSubmit={handleCreate}>
          {error && <p className="form-error">{error}</p>}

          <label>Sarlavha</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Masalan: Poyezddagi jumboq"
            required
          />

          <label>Tavsif (o'yinchiga ko'rinadi)</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            required
          />

          <label>Yechim (MAXFIY — faqat sizga va hamkoringizga ko'rinadi)</label>
          <textarea
            value={solution}
            onChange={(e) => setSolution(e.target.value)}
            rows={3}
            required
          />

          <button type="submit" disabled={creating}>
            {creating ? 'Yaratilmoqda...' : 'Yaratish'}
          </button>
        </form>
      )}

      <div className="my-case-grid">
        {cases.map((c) => (
          <div key={c.id} className="my-case-card" onClick={() => navigate(`/my-cases/${c.id}/edit`)}>
            <div className="my-case-card-header">
              <h2>{c.title}</h2>
              {c.is_owner ? (
                <span className="badge owner">Egasi</span>
              ) : (
                <span className="badge collaborator">Hamkor</span>
              )}
            </div>
            <p>{c.description}</p>
            <span className={`status ${c.is_active ? 'active' : 'draft'}`}>
              {c.is_active ? 'Faol (o\'yinda ko\'rinadi)' : 'Qoralama'}
            </span>
          </div>
        ))}
      </div>

      {cases.length === 0 && !showForm && (
        <p className="empty-hint">Hali case yaratmagansiz. "+ Yangi case" tugmasini bosing.</p>
      )}
    </div>
  );
}

export default MyCasesPage;