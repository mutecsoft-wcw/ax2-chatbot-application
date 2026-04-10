import React, { createContext, useState, useCallback } from 'react';

export const SessionContext = createContext();

export const SessionProvider = ({ children }) => {
    // 초기값을 null이나 랜덤 ID가 아닌, 서버가 쓰는 'default_session'으로 설정
    const [sessionId, setSessionId] = useState(() =>
        localStorage.getItem('chatSessionId') || 'default_session'
    );

    // 서버 응답에 맞춰 세션을 갱신하는 단일 통로
    const updateSession = useCallback((newId) => {
        if (newId && newId !== sessionId) {
            console.log("💾 세션 ID 갱신:", newId);
            localStorage.setItem('chatSessionId', newId);
            setSessionId(newId);
        }
    }, [sessionId]);

    return (
        <SessionContext.Provider value={{ sessionId, updateSession }}>
            {children}
        </SessionContext.Provider>
    );
};