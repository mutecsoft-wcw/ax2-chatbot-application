import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SessionContext } from '../context/SessionContext';
import * as Styles from '../style/ChatStyles';
import '../css/ChatWindow.css';
import { responseInterceptor } from '../utils/ResponseInterceptor';
import { useChatInit } from '../hooks/useChatInit';
import { useChatActions } from '../hooks/useChatActions';

const ChatWindow = () => {
    const { sessionId, updateSession } = useContext(SessionContext);
    const sessionIdRef = useRef(sessionId);
    const updateSessionRef = useRef(updateSession);

    const location = useLocation();
    const navigate = useNavigate();
    const chatRef = useRef(null);

    const {
        isLoaded,
        initialHistory,
        initialQuery,
        isProcessed
    } = useChatInit(sessionId, updateSession, location, navigate);
    
    useChatActions(chatRef);

    useEffect(() => {
        sessionIdRef.current = sessionId;
        updateSessionRef.current = updateSession;
    }, [sessionId, updateSession]);

    const memoizedChat = useMemo(() => {
        if (!isLoaded) return null;

        return (
            <DeepChat
                ref={chatRef}
                style={Styles.chatComponentStyle}
                history={initialHistory} 
                stream={true}
                scrollButton={Styles.scrollBtnStyles}
                onComponentRender={(chatElement) => {
                    if (!isProcessed.current && initialQuery.current) {
                        isProcessed.current = true;
                        setTimeout(() => {
                            chatElement.submitUserMessage({ text: initialQuery.current });
                            initialQuery.current = null;
                        }, 100);
                    }
                }}
                connect={{
                    url: `${process.env.REACT_APP_INTERNAL_API_URL}/public/stream-chat`,
                    method: 'POST',
                    stream: 'sse'
                }}
                requestInterceptor={(details) => {
                    if (!details.body) return details;
                    try {
                        const currentBody = typeof details.body === 'string'
                            ? JSON.parse(details.body)
                            : details.body;

                        const finalPayload = {
                            messages: (currentBody.messages || []).map(msg => ({
                                role: msg.role || 'user',
                                text: msg.text || msg.content || ""
                            })),
                            sessionId: sessionIdRef.current || ""
                        };
                        details.body = finalPayload;
                    } catch (e) {
                        console.error("인터셉터 처리 중 에러:", e);
                    }
                    return details;
                }}
                responseInterceptor={(response) => {
                    if (response?.sessionId) updateSessionRef.current(response.sessionId);
                    return responseInterceptor(response);
                }}
                messageStyles={Styles.messageStyle}
                textInput={Styles.textInputStyle}
                inputAreaStyle={Styles.inputAreaStyles}
                submitButtonStyles={Styles.submitButtonStyles}
            />
        );
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isLoaded, initialHistory]);


    return (
        <div className="container">
            <div className="header">
                <span className="header-title">조사 업무 지원 AI 챗봇</span>
            </div>

            {isLoaded ? memoizedChat : (
                <div className="loading-container"><p>로딩 중...</p></div>
            )}
        </div>
    );
};

export default ChatWindow;