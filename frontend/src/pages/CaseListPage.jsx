import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCases } from '../api/cases';
import './CaseListPage.css';

function CaseListPage() {
  const [cases, setCases] = useState([]);   // backend'dan kelgan case'lar ro'yxati
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate(); // boshqa sahifaga o'tish uchun

  // useEffect — komponent birinchi marta ekranga chiqqanda ishga tushadigan kod.
  // Bo'sh massiv [] degani — bu kod faqat BIR MARTA, sahifa ochilganda ishlaydi.
  useEffect(() => {
    async function loadCases() {
      try {
        const data = await getCases();
        setCases(data);
      } catch (err) {
        console.error(err);
        setError("Case'larni yuklab bo'lmadi. Backend server ishlayotganini tekshiring.");
      } finally {
        setLoading(false);
      }
    }

    loadCases();
  }, []);

  function handleCaseClick(caseId) {
    navigate(`/case/${caseId}`); // shu case'ning tafsilot sahifasiga o'tamiz
  }

  if (loading) return <div className="status-message">Yuklanmoqda...</div>;
  if (error) return <div className="status-message error">{error}</div>;

  return (
    <div className="case-list-page">
      <h1>AI Detective</h1>
      <p className="subtitle">Tergov qilish uchun ishni tanlang</p>

      <div className="case-grid">
        {cases.map((c) => (
          <div key={c.id} className="case-card" onClick={() => handleCaseClick(c.id)}>
            <h2>{c.title}</h2>
            <p>{c.description}</p>
          </div>
        ))}
      </div>

      {cases.length === 0 && <p>Hozircha ishlar mavjud emas.</p>}
    </div>
  );
}

export default CaseListPage;