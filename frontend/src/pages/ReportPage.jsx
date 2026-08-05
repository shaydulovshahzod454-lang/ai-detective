import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { submitReport } from '../api/reports';
import './ReportPage.css';

function getSessionId() {
  return sessionStorage.getItem('ai_detective_session') || 'unknown-session';
}

function ReportPage() {
  const { caseId } = useParams();
  const navigate = useNavigate();

  const [accusedName, setAccusedName] = useState('');
  const [reasoning, setReasoning] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  async function handleSubmit() {
    if (!accusedName.trim() || !reasoning.trim()) return;

    setSubmitting(true);
    try {
      const data = await submitReport(caseId, getSessionId(), accusedName, reasoning);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  // Agar natija kelgan bo'lsa — baholash ekranini ko'rsatamiz
  if (result) {
    return (
      <div className="report-page">
        <div className={`result-card ${result.is_correct ? 'correct' : 'incorrect'}`}>
          <h1>{result.is_correct ? '✅ To\'g\'ri topdingiz!' : '❌ Noto\'g\'ri'}</h1>
          <p>{result.ai_feedback}</p>
          <button onClick={() => navigate('/')}>Bosh sahifaga qaytish</button>
        </div>
      </div>
    );
  }

  return (
    <div className="report-page">
      <button className="back-button" onClick={() => navigate(`/case/${caseId}`)}>
        ← Orqaga
      </button>

      <h1>Yakuniy hisobot</h1>
      <p className="report-hint">
        To'plagan dalillaringiz asosida, kim aybdor ekanini va nima uchun shunday
        deb o'ylayotganingizni yozing.
      </p>

      <label>Aybdor deb hisoblaysiz:</label>
      <input
        type="text"
        value={accusedName}
        onChange={(e) => setAccusedName(e.target.value)}
        placeholder="Masalan: Bog'bon Qodir"
      />

      <label>Asoslashingiz:</label>
      <textarea
        value={reasoning}
        onChange={(e) => setReasoning(e.target.value)}
        placeholder="Nima uchun aynan shu odam aybdor deb o'ylaysiz?"
        rows={6}
      />

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={submitting || !accusedName.trim() || !reasoning.trim()}
      >
        {submitting ? 'Tekshirilmoqda...' : 'Hisobotni topshirish'}
      </button>
    </div>
  );
}

export default ReportPage;