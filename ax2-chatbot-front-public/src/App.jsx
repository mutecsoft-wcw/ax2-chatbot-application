import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'; 
import { SessionProvider } from './context/SessionContext';
import Header from './layout/Header';
import Main from './layout/Main';
import ChatWindow from './components/ChatWindow';
import Test from './components/Test';
import Example1 from './components/example/Example1';
import Example2 from './components/example/Example2';
import ExampleChat1 from './components/example/ExampleChat1';
import ExampleChat2 from './components/example/ExampleChat2';


function AppContent() {
    const navigate = useNavigate();

    const handleSearch = (query) => {
        if (!query.trim()) return;
        navigate('/chat', { state: { initialMessage: query }});
    };

    return (
        <div className="App" style={{ display: 'flex', flexDirection: 'column', height: '100dvh' }}>
            {/* <Header onLogoClick={() => navigate('/')} /> */}
            <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <Routes>
                    <Route path="/" element={<Main onSearch={handleSearch} />} />
                    <Route path="/chat" element={<ChatWindow />} />
                    <Route path="/test" element={<Test />} />
                    <Route path="/example1" element={<Example1 />} />
                    <Route path="/example2" element={<Example2 />} />
                    <Route path="/example1/chat" element={<ExampleChat1 />} />
                    <Route path="/example2/chat" element={<ExampleChat2 />} />
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