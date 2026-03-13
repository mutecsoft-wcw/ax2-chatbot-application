
import Header from './route/Header';
import Footer from './route/Footer';
import Main from './route/Main';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <div className="App" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh' 
    }}>
      <Header />
      
      <Main>
        <ChatWindow />
      </Main>

      <Footer />
    </div>
  );
}

export default App;