import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCaseDetail } from '../api/cases';
import './CaseDetailPage.css';

function CaseDetailPage() {
  // useParams — URL manzildagi ':caseId' qismini o'qib oladi
  // Masalan URL /case/3 bo'lsa, caseId = "3" bo'ladi
  const { caseId } = useParams();
  const navigate = useNavigate();

  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCase() {
      try {
        const data = await getCaseDetail(caseId);
        setCaseData(data);
      } catch (err) {
        console.error(err);
        setError("Case ma'lumotini yuklab bo'lmadi.");
      } finally {
        setLoading(false);
      }
    }

    loadCase();
  }, [caseId]); // caseId o'zgarsa (masalan boshqa case ochilsa), qayta yuklaydi

  function handleCharacterClick(characterId) {
    navigate(`/case/${caseId}/character/${characterId}`);
  }

  if (loading) return <div className="status-message">Yuklanmoqda...</div>;
  if (error) return <div className="status-message error">{error}</div>;
  if (!caseData) return null;

  return (
    <div className="case-detail-page">
      <button className="back-button" onClick={() => navigate('/')}>
        ← Orqaga
      </button>

      <h1>{caseData.title}</h1>
      <p className="case-description">{caseData.description}</p>

      {caseData.scenes.map((scene) => (
        <div key={scene.id} className="scene-block">
          <h2>{scene.name}</h2>
          <p className="scene-description">{scene.description}</p>

          <div className="character-grid">
            {scene.characters.map((character) => (
              <div
                key={character.id}
                className="character-card"
                onClick={() => handleCharacterClick(character.id)}
              >
                {character.image ? (
                  <img src={character.image} alt={character.name} />
                ) : (
                  <div className="character-placeholder">👤</div>
                )}
                <p>{character.name}</p>
              </div>
            ))}
          </div>
        </div>
      ))}
      <button
        className="write-report-button"
        onClick={() => navigate(`/case/${caseId}/report`)}
      >
        📝 Hisobot yozish
      </button>
    </div>
    
  );
}

export default CaseDetailPage;