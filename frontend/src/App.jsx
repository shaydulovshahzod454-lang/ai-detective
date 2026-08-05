import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CaseListPage from './pages/CaseListPage';
import CaseDetailPage from './pages/CaseDetailPage';
import ChatPage from './pages/ChatPage';
import ReportPage from './pages/ReportPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CaseListPage />} />
        <Route path="/case/:caseId" element={<CaseDetailPage />} />
        <Route path="/case/:caseId/character/:characterId" element={<ChatPage />} />
        <Route path="/case/:caseId/report" element={<ReportPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;