import React, { useState } from 'react';
import '../css/Main.css';
import { FaSearch } from "react-icons/fa";

const Main = ({ onSearch, isLoading }) => {
    const [inputValue, setInputValue] = useState("");

    const handleSearchClick = (text) => {
        if (!text.trim() || isLoading) return;

        if (onSearch) onSearch(text);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.nativeEvent.isComposing) {
            handleSearchClick(inputValue);
        }
    };

    return (
        <div className="main-container">
            <div className="search-section">
                <h1 className="main-title">
                    궁금하신 건강정보가 <br /> 있으신가요?
                </h1>

                <div className="search-box">
                    <input
                        type="text"
                        className="search-input"
                        placeholder={isLoading ? "세션 연결 중..." : "검색어를 입력하세요."}
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading} // 세션 발급 전 입력 방지
                        enterKeyHint="search"
                    />
                    <button
                        className="search-icon-btn"
                        onClick={() => handleSearchClick(inputValue)}
                        disabled={isLoading || !inputValue.trim()}
                    >
                        <FaSearch />
                    </button>
                </div>

                <div className="hash-tags">
                    {[].map(tag => (
                        <span
                            key={tag}
                            className="tag"
                            onClick={() => handleSearchClick(tag)}
                            style={{
                                cursor: isLoading ? 'wait' : 'pointer',
                                opacity: isLoading ? 0.6 : 1
                            }}
                        >
                            #{tag}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Main;