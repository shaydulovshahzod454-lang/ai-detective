import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import CaseListPage from './pages/CaseListPage';
import CaseDetailPage from './pages/CaseDetailPage';
import ChatPage from './pages/ChatPage';
import ReportPage from './pages/ReportPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MyCasesPage from './pages/MyCasesPage';
import CaseEditPage from './pages/CaseEditPage';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<CaseListPage />} />
          <Route path="/case/:caseId" element={<CaseDetailPage />} />
          <Route path="/case/:caseId/character/:characterId" element={<ChatPage />} />
          <Route path="/case/:caseId/report" element={<ReportPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/my-cases" element={<MyCasesPage />} />
          {/* /my-cases/:caseId/edit keyingi bosqichda qo'shiladi */}
          <Route path="/my-cases/:caseId/edit" element={<CaseEditPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;