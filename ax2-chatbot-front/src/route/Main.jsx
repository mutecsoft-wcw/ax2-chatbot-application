import React, { useState } from 'react';
import '../css/Main.css';

const Main = ({ onSearch }) => {
  const [inputValue, setInputValue] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSearch(inputValue);
    }
  };

  return (
    <div className="main-container">
      <div className="search-section">
        <h1 className="main-title">
          궁금하신 건강정보가<br />있으신가요?
        </h1>
        
        <div className="search-box">
          <input
            type="text"
            className="search-input"
            placeholder="궁금하신 건강 관련 검색어를 입력하세요."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button className="search-icon-btn" onClick={() => onSearch(inputValue)}>
            🔍
          </button>
        </div>

        <div className="hash-tags">
          <span onClick={() => onSearch("고혈압 원인")}>#고혈압 원인</span>
          <span onClick={() => onSearch("우울증 원인")}>#우울증 원인</span>
          <span onClick={() => onSearch("당뇨병 증상")}>#당뇨병 증상</span>
        </div>
      </div>
    </div>
  );
};

export default Main;