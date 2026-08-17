import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { sendMessage } from '../api/chat';
import { getClues, addClue, deleteClue } from '../api/clues';
import ClueSidebar from '../components/ClueSidebar';
import './ChatPage.css';

function getSessionId() {
  let sessionId = sessionStorage.getItem('ai_detective_session');
  if (!sessionId) {
    sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).slice(2);
    sessionStorage.setItem('ai_detective_session', sessionId);
  }
  return sessionId;
}

function ChatPage() {
  const { caseId, characterId } = useParams();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [clues, setClues] = useState([]);

  const messagesEndRef = useRef(null);
  const sessionId = getSessionId();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Sahifa ochilganda shu case uchun mavjud dalillarni yuklaymiz
  useEffect(() => {
    async function loadClues() {
      try {
        const data = await getClues(caseId, sessionId);
        setClues(data);
      } catch (err) {
        console.error(err);
      }
    }
    loadClues();
  }, [caseId, sessionId]);

  async function handleSend() {
    const text = input.trim();
    if (!text || sending) return;

    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    setInput('');
    setSending(true);

    try {
      const aiResponse = await sendMessage(characterId, text, sessionId);
      setMessages((prev) => [...prev, { role: 'assistant', content: aiResponse }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '(Xatolik yuz berdi, qayta urinib ko\'ring)' },
      ]);
    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  // Xabarni dalil sifatida saqlaydi
  async function handleSaveAsClue(messageText) {
    try {
      const newClue = await addClue(caseId, sessionId, messageText, characterId);
      setClues((prev) => [...prev, newClue]);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleDeleteClue(clueId) {
    try {
      await deleteClue(clueId, sessionId);
      setClues((prev) => prev.filter((c) => c.id !== clueId));
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="chat-page-layout">
      <div className="chat-page">
        <button className="back-button" onClick={() => navigate(`/case/${caseId}`)}>
          ← Orqaga
        </button>

        <div className="chat-window">
          {messages.length === 0 && (
            <p className="chat-hint">Personajga savol berib, so'roqni boshlang...</p>
          )}

          {messages.map((msg, index) => (
            <div key={index} className={`chat-bubble ${msg.role}`}>
              <p>{msg.content}</p>
              {msg.role === 'assistant' && (
                <button
                  className="save-clue-button"
                  onClick={() => handleSaveAsClue(msg.content)}
                >
                  🔍 Dalil sifatida saqlash
                </button>
              )}
            </div>
          ))}

          {sending && <div className="chat-bubble assistant typing">Yozmoqda...</div>}

          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Savolingizni yozing... (Enter — yuborish)"
            rows={2}
          />
          <button onClick={handleSend} disabled={sending}>
            Yuborish
          </button>
        </div>
      </div>

      <ClueSidebar clues={clues} onDelete={handleDeleteClue} />
    </div>
  );
}

export default ChatPage;