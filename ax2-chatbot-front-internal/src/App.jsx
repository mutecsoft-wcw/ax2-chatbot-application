import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'; 
import { SessionProvider } from './context/SessionContext';
import Header from './route/Header';
import Main from './route/Main';
import ChatWindow from './components/ChatWindow';

function AppContent() {
    const navigate = useNavigate();

    const handleSearch = (query) => {
        if (!query.trim()) return;
        navigate('/chat', { state: { initialMessage: query }});
    };

    return (
        <div className="App" style={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
            <Header onLogoClick={() => navigate('/')} />
            <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <Routes>
                    <Route path="/" element={<Main onSearch={handleSearch} />} />
                    <Route path="/chat" element={<ChatWindow />} />
                </Routes>
            </main>
        </div>
    );
}

function App() {
    return (
        <Router>
            <SessionProvider>
                <AppContent />
            </SessionProvider>
        </Router>
    );
}

export default App;