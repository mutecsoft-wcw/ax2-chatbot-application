import React, { createContext, useState, useCallback } from 'react';

export const SessionContext = createContext();

export const SessionProvider = ({ children }) => {
    const [sessionId, setSessionId] = useState(() =>
        localStorage.getItem('chatSessionId') || ''
    );

    const updateSession = useCallback((newId) => {
        if (newId && newId !== sessionId) {
            console.log("세션 ID 갱신:", newId);
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