import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSearch } from 'react-icons/fa';
import Icon from '../../icon/Icon';
import '../../css/example/Example1.css';

const Example1 = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="header-in">
          <div className="logo-group">
            <Icon type="mark" height={36} /> 
            <div className="v-line"></div>
            <h1 className="header-title1">건강지기 AI 챗봇</h1>
          </div>
        </div>
      </header>

      {/* 중앙 섹션 */}
      <main className="hero-section">
        <h1 className="main-title">궁금하신 건강정보가<br /> 있으신가요?</h1>
        
        <div className="search-container">
          <input 
            type="text" 
            placeholder="검색어를 입력하세요." 
            className="search-input"
            onClick={() => navigate('/example1/chat')}
          />
          <button className="search-button">
            <FaSearch />
          </button>
        </div>

        <div className="hash-tags">
                    {["당뇨병 식단", "간단 건강 설문", "건강 개선 설문"].map(tag => (
                        <span
                            key={tag}
                            className="tag"
                        >
                            #{tag}
                        </span>
                    ))}
                </div>
      </main>
    </div>
  );
};

export default Example1;