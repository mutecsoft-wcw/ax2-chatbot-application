import React, { useContext, useEffect, useRef, useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SessionContext } from '../context/SessionContext';
import { chatApi } from '../api/chatApi';
import * as Styles from '../style/ChatStyles';
import FileUploadModal from './modal/FileUploadModal';

const ChatWindow = () => {
    const { sessionId, updateSession } = useContext(SessionContext);
    const location = useLocation();
    const navigate = useNavigate();
    const chatRef = useRef(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

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
    }, [sessionId, isLoaded]);

    const handleFileUpload = async (file) => {
        console.log("서버로 전송할 파일:", file.name);

        // TODO[wcw] 파일 업로드 API 호출
        // await chatApi.uploadReport(file, sessionId);

        setTimeout(() => {
            if (chatRef.current) {
                console.log("메시지 전송 시도:", file.name);

                // submitUserMessage 호출
                chatRef.current.submitUserMessage({
                    text: `[파일 업로드 완료] ${file.name} 분석을 시작해줘.`,
                });
            } else {
                console.error("파일 업로드 에러");
            }
        }, 300);
    };

    return (
        <div style={Styles.containerStyle}>
            <div style={Styles.uploadHeaderStyle}>
                <span style={Styles.headerTitleStyle}>대국민 챗봇</span>
                <button
                    onClick={() => setIsModalOpen(true)}
                    style={Styles.uploadButton}
                >
                    📄 리포트 업로드
                </button>
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
                        url: process.env.REACT_APP_PUBLIC_API_URL,
                        method: 'POST',
                        stream: 'sse'
                    }}
                    requestInterceptor={(details) => {
                        if (!details.body) return details;

                        try {
                            // 현재 바디 파싱 (문자열일 경우만)
                            const currentBody = typeof details.body === 'string'
                                ? JSON.parse(details.body)
                                : details.body;

                            // 서버 모델 LlmRequest 규격
                            const finalPayload = {
                                messages: (currentBody.messages || []).map(msg => ({
                                    role: msg.role || 'user',
                                    text: msg.text || msg.content || ""
                                })),
                                sessionId: sessionId || "default_session"
                            };
                            details.body = finalPayload;
                        } catch (e) {
                            console.error("인터셉터 처리 중 에러:", e);
                        }
                        return details;
                    }}
                    responseInterceptor={(response) => {
                        if (response?.sessionId) updateSession(response.sessionId);
                        return response;
                    }}
                    messageStyles={{
                        default: {
                            shared: {
                                bubble: {
                                    borderRadius: '10px',
                                    padding: '10px 14px',
                                },
                            },
                            user: {
                                bubble: {
                                    backgroundColor: 'var(--gok-blue)',
                                    color: 'white',
                                },
                            },
                            ai: {
                                bubble: {
                                    backgroundColor: '#F0F2F5',
                                    color: '#333333',
                                },
                            },
                        },
                    }}
                    textInput={{
                        placeholder: {
                            text: '검색어를 입력하세요...',
                            style: { color: '#bcbcbc' }
                        },
                        style: {
                            borderRadius: '20px',
                            border: '1px solid #e0e0e0',
                            backgroundColor: 'white',
                            padding: '10px',
                        }
                    }}

                    submitButtonStyles={{
                        position: 'outside-right',
                        submit: {
                            containerStyle: {
                                backgroundColor: '#4A7DFF',
                                borderRadius: '10px',
                                width: '60px',
                                height: '40px',
                                marginLeft: '10px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'pointer',
                                border: 'none',
                            },
                            svg: { content: '' },
                            text: {
                                content: '전송',
                                style: {
                                    color: 'white',
                                    fontSize: '14px',
                                    fontWeight: 'bold',
                                }
                            }
                        },
                        loading: {
                            containerStyle: { backgroundColor: '#a5c0ff' },
                            svg: { content: '' }
                        }
                    }}
                />
            ) : (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <p>대화 내용을 불러오는 중입니다...</p>
                </div>
            )}
            <FileUploadModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onUpload={handleFileUpload}
            />
        </div>
    );
};

export default ChatWindow;