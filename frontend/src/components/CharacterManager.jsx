import { useState, useEffect } from 'react';
import { getCharacters, createCharacter, updateCharacter, deleteCharacter } from '../api/caseContent';
import { getScenes } from '../api/caseContent';
import RichTextEditor from './RichTextEditor';

function CharacterManager({ caseId }) {
  const [characters, setCharacters] = useState([]);
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState('');
  const [expandedId, setExpandedId] = useState(null); // qaysi personaj "ochiq" ko'rinishda

  useEffect(() => {
    async function load() {
      const [charData, sceneData] = await Promise.all([
        getCharacters(caseId), getScenes(caseId),
      ]);
      setCharacters(charData);
      setScenes(sceneData);
      setLoading(false);
    }
    load();
  }, []);

  async function handleAdd(e) {
  e.preventDefault();
  if (!newName.trim()) return;
  try {
    const character = await createCharacter(caseId, {
      name: newName, personality: '', knowledge: '', secrets: '',
    });
    setCharacters((prev) => [...prev, character]);
    setNewName('');
    setExpandedId(character.id);
  } catch (err) {
    console.error(err.response?.data || err);
    alert("Xatolik yuz berdi, konsolni tekshiring.");
  }
}

  async function handleUpdate(charId, field, value) {
    const updated = await updateCharacter(caseId, charId, { [field]: value });
    setCharacters((prev) => prev.map((c) => (c.id === charId ? updated : c)));
  }

  async function handleDelete(charId) {
    if (!confirm("Bu personajni o'chirishga ishonchingiz komilmi?")) return;
    await deleteCharacter(caseId, charId);
    setCharacters((prev) => prev.filter((c) => c.id !== charId));
  }

  async function handleImageUpload(charId, file) {
    const formData = new FormData();
    formData.append('image', file);
    const updated = await updateCharacter(caseId, charId, formData);
    setCharacters((prev) => prev.map((c) => (c.id === charId ? updated : c)));
  }

  if (loading) return <p>Yuklanmoqda...</p>;

  return (
    <div className="content-manager">
      <form className="inline-add-form" onSubmit={handleAdd}>
        <input
          placeholder="Yangi personaj ismi"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <button type="submit">+ Qo'shish</button>
      </form>

      {characters.map((char) => (
        <div key={char.id} className="content-item">
          <div className="content-item-header" onClick={() => setExpandedId(expandedId === char.id ? null : char.id)}>
            <strong>{char.name}</strong>
            {char.is_guilty && <span className="guilty-badge">Aybdor</span>}
            <span className="expand-arrow">{expandedId === char.id ? '▲' : '▼'}</span>
          </div>

          {expandedId === char.id && (
            <div className="content-item-body" onClick={(e) => e.stopPropagation()}>
              <label>Ism</label>
              <input
                defaultValue={char.name}
                onBlur={(e) => handleUpdate(char.id, 'name', e.target.value)}
              />

              <label>Rasm</label>
              <div className="image-upload-row">
                {char.image && <img src={char.image} alt={char.name} className="preview-image round" />}
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => e.target.files[0] && handleImageUpload(char.id, e.target.files[0])}
                />
              </div>

              <label>Qaysi joyda</label>
              <select
                defaultValue={char.scene || ''}
                onChange={(e) => handleUpdate(char.id, 'scene', e.target.value || null)}
              >
                <option value="">— Tanlanmagan —</option>
                {scenes.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>

              <label>Xarakter</label>
              <RichTextEditor
                value={char.personality}
                onChange={(html) => handleUpdate(char.id, 'personality', html)}
                placeholder="Personajning xarakteri, gapirish uslubi..."
              />

              <label>Bilim (nima biladi)</label>
              <RichTextEditor
                value={char.knowledge}
                onChange={(html) => handleUpdate(char.id, 'knowledge', html)}
                placeholder="Personaj biladigan ma'lumotlar..."
              />

              <label>Sirlar</label>
              <RichTextEditor
                value={char.secrets}
                onChange={(html) => handleUpdate(char.id, 'secrets', html)}
                placeholder="Personaj yashiradigan sirlar..."
              />

              <label>Alibi</label>
              <RichTextEditor
                value={char.alibi}
                onChange={(html) => handleUpdate(char.id, 'alibi', html)}
                placeholder="Voqea kuni qayerda, qachon nima qilgani..."
              />

              <label>Munosabatlar</label>
              <RichTextEditor
                value={char.relationships}
                onChange={(html) => handleUpdate(char.id, 'relationships', html)}
                placeholder="Boshqa personajlar bilan munosabati..."
              />

              <label>Yolg'on darajasi</label>
              <select
                defaultValue={char.lying_tendency}
                onChange={(e) => handleUpdate(char.id, 'lying_tendency', e.target.value)}
              >
                <option value="honest">Har doim rost gapiradi</option>
                <option value="evasive">Chalg'itadi, lekin yolg'on gapirmaydi</option>
                <option value="deceptive">Kerak bo'lsa yolg'on gapiradi</option>
              </select>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  defaultChecked={char.is_guilty}
                  onChange={(e) => handleUpdate(char.id, 'is_guilty', e.target.checked)}
                />
                Bu personaj aybdor
              </label>

              <button className="delete-btn" onClick={() => handleDelete(char.id)}>
                Personajni o'chirish
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default CharacterManager;