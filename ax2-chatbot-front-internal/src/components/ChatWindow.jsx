import React, { useContext, useEffect, useRef, useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SessionContext } from '../context/SessionContext';
import { chatApi } from '../api/chatApi';
import * as Styles from '../style/ChatStyles';
import '../css/ChatWindow.css';
import { responseInterceptor } from '../utils/ResponseInterceptor';

const ChatWindow = () => { 
    const { sessionId, updateSession } = useContext(SessionContext);
    const location = useLocation();
    const navigate = useNavigate();
    const chatRef = useRef(null);

    // 로딩 상태 관리
    const [isLoaded, setIsLoaded] = useState(false);

    const initialHistory = useRef([]);
    const initialQuery = useRef(location.state?.initialMessage || null);
    const isProcessed = useRef(false);
    const isInitialMount = useRef(true);

    useEffect(() => {
        if (isLoaded || !isInitialMount.current) return;
        const initChat = async () => {
            try {
                // 서버에서 히스토리 가져오기
                const res = await chatApi.fetchHistory(sessionId);
                const data = res?.data || res;
                if (data) {
                    if (data.sessionId && data.sessionId !== sessionId) {
                        updateSession(data.sessionId);
                    }
                    initialHistory.current = data.history || [];
                }
            } catch (err) {
                console.error("데이터 로드 실패:", err);
            } finally {
                isInitialMount.current = false;
                setIsLoaded(true);

                if (location.state?.initialMessage) {
                    navigate(location.pathname, { replace: true, state: {} });
                }
            }
        };
        initChat();
    }, [sessionId, updateSession, navigate, location.pathname, location.state?.initialMessage, isLoaded]);

    return (
        <div className="container">
            <div className="header">
                <span className="header-title">조사 지원 챗봇</span>
            </div>

            {isLoaded ? (
                <DeepChat
                    ref={chatRef}
                    style={Styles.chatComponentStyle}
                    history={initialHistory.current}
                    stream={true}
                    scrollButton="true"
                    onComponentRender={(chatElement) => {
                        // 딱 한 번만 실행되도록 제어
                        if (!isProcessed.current && initialQuery.current) {
                            isProcessed.current = true;
                            console.log("신규 질문 전송:", initialQuery.current);

                            // 렌더링이 완전히 끝난 후 전송
                            setTimeout(() => {
                                chatElement.submitUserMessage({ text: initialQuery.current });
                                initialQuery.current = null; // 전송 후 비움
                            }, 1000);
                        }
                    }}
                    connect={{
                        url: process.env.REACT_APP_INTERNAL_API_URL,
                        method: 'POST',
                        stream: 'sse'
                    }}
                    requestInterceptor={(details) => {
                        if (!details.body) return details;

                        try {
                            const currentBody = typeof details.body === 'string'
                                ? JSON.parse(details.body)
                                : details.body;

                            // 서버 모델 LlmRequest 규격
                            const finalPayload = {
                                messages: (currentBody.messages || []).map(msg => ({
                                    role: msg.role || 'user',
                                    text: msg.text || msg.content || ""
                                })),
                                sessionId: sessionId || ""
                            };
                            details.body = finalPayload;
                        } catch (e) {
                            console.error("인터셉터 처리 중 에러:", e);
                        }
                        return details;
                    }}
                    responseInterceptor={(response) => {
                        if (response?.sessionId) updateSession(response.sessionId);
                        return responseInterceptor(response);
                    }}
                    messageStyles={Styles.messageStyle}
                    textInput={Styles.textInputStyle}

                    submitButtonStyles={Styles.submitButtonStyle}
                />
            ) : (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <p>대화 내용을 불러오는 중입니다...</p>
                </div>
            )}
        </div>
    );
};

export default ChatWindow;