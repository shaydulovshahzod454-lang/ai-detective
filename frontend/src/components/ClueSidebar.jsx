import './ClueSidebar.css';

function ClueSidebar({ clues, onDelete }) {
  return (
    <div className="clue-sidebar">
      <h3>🔍 Dalillar ({clues.length})</h3>

      {clues.length === 0 && <p className="clue-empty">Hali dalil yo'q</p>}

      <div className="clue-list">
        {clues.map((clue) => (
          <div key={clue.id} className="clue-item">
            <p>{clue.text}</p>
            {clue.source_character_name && (
              <span className="clue-source">— {clue.source_character_name}</span>
            )}
            <button className="clue-delete" onClick={() => onDelete(clue.id)}>
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ClueSidebar;