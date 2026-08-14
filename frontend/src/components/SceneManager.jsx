import { useState, useEffect } from 'react';
import { getScenes, createScene, updateScene, deleteScene } from '../api/caseContent';

function SceneManager({ caseId }) {
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState('');

  useEffect(() => {
    loadScenes();
  }, []);

  async function loadScenes() {
    try {
      const data = await getScenes(caseId);
      setScenes(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd(e) {
  e.preventDefault();
  if (!newName.trim()) return;
  try {
    const scene = await createScene(caseId, { name: newName, description: '' });
    setScenes((prev) => [...prev, scene]);
    setNewName('');
  } catch (err) {
    console.error(err.response?.data || err);
    alert("Xatolik yuz berdi, konsolni tekshiring.");
  }
}

  async function handleUpdate(sceneId, field, value) {
    const updated = await updateScene(caseId, sceneId, { [field]: value });
    setScenes((prev) => prev.map((s) => (s.id === sceneId ? updated : s)));
  }

  async function handleDelete(sceneId) {
    if (!confirm("Bu joyni o'chirishga ishonchingiz komilmi?")) return;
    await deleteScene(caseId, sceneId);
    setScenes((prev) => prev.filter((s) => s.id !== sceneId));
  }

  async function handleImageUpload(sceneId, file) {
    const formData = new FormData();
    formData.append('background_image', file);
    const updated = await updateScene(caseId, sceneId, formData);
    setScenes((prev) => prev.map((s) => (s.id === sceneId ? updated : s)));
  }

  if (loading) return <p>Yuklanmoqda...</p>;

  return (
    <div className="content-manager">
      <form className="inline-add-form" onSubmit={handleAdd}>
        <input
          placeholder="Yangi joy nomi (masalan: Kutubxona)"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <button type="submit">+ Qo'shish</button>
      </form>

      {scenes.map((scene) => (
        <div key={scene.id} className="content-item">
          <div className="content-item-header">
            <input
              className="item-title-input"
              defaultValue={scene.name}
              onBlur={(e) => handleUpdate(scene.id, 'name', e.target.value)}
            />
            <button className="delete-btn" onClick={() => handleDelete(scene.id)}>O'chirish</button>
          </div>

          <textarea
            placeholder="Tavsif..."
            defaultValue={scene.description}
            onBlur={(e) => handleUpdate(scene.id, 'description', e.target.value)}
            rows={2}
          />

          <div className="image-upload-row">
            {scene.background_image && (
              <img src={scene.background_image} alt={scene.name} className="preview-image" />
            )}
            <input
              type="file"
              accept="image/*"
              onChange={(e) => e.target.files[0] && handleImageUpload(scene.id, e.target.files[0])}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

export default SceneManager;