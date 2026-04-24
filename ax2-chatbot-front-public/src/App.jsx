import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'; 
import { SessionProvider } from './context/SessionContext';
import Header from './layout/Header';
import Main from './layout/Main';
import ChatWindow from './components/ChatWindow';
import Test from './components/Test';

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
                    <Route path="/test" element={<Test />} />
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