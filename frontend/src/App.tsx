import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import { useSessionStore } from './store/sessionStore';
import MainLayout from './components/layout/MainLayout';
import Home from './pages/Home';
import Generator from './pages/Generator';
import Preview from './pages/Preview';

function App() {
  const { sessionId, loadSession, createSession } = useSessionStore();

  useEffect(() => {
    // Initialize session on app load
    if (sessionId) {
      loadSession(sessionId);
    } else {
      createSession();
    }
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="generator/:docType" element={<Generator />} />
          <Route path="preview" element={<Preview />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
