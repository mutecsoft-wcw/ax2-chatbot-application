import React, { useEffect, useState } from 'react';
import Header from './route/Header';
import Footer from './route/Footer';
import Main from './route/Main'; // 초기 화면 디자인이 담긴 컴포넌트
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  // 채팅창 활성화 여부와 초기 검색어를 관리하는 상태
  const [isChatActive, setIsChatActive] = useState(() => {
    return localStorage.getItem("isChatActive") === "true";
  });
  const [initialQuery, setInitialQuery] = useState(() => {
    return localStorage.getItem("initialQuery") || "";
  });

  const goToMain = () => {
    setIsChatActive(false);
    setInitialQuery("");
    localStorage.removeItem("isChatActive");
    localStorage.removeItem("initialQuery");
    localStorage.removeItem("chatHistory");
  };

  useEffect(() => {
    localStorage.setItem("isChatActive", isChatActive);
    localStorage.setItem("initialQuery", initialQuery);
  
  }, [isChatActive, initialQuery]);

  return (
    <div className="App" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      backgroundColor: '#f4f7f9' 
    }}>
      <Header onLogoClick={goToMain} />
      
      {/* 상태에 따라 Main(초기화면) 또는 ChatWindow를 렌더링 */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {!isChatActive ? (
          // 초기 화면: 검색 함수를 props로 전달
          <Main onSearch={(query) => {
            setInitialQuery(query);
            setIsChatActive(true);
          }} />
        ) : (
          // 채팅 화면: 초기 검색어를 props로 전달
          <ChatWindow initialMessage={initialQuery} />
        )}
      </div>

      <Footer />
    </div>
  );
}

export default App;