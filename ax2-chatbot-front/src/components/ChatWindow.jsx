import React, { useContext, useEffect, useRef, useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SessionContext } from '../context/SessionContext';
import { chatApi } from '../api/chatApi';
import * as Styles from '../style/ChatStyles';
import FileUploadModal from './modal/FileUploadModal';
import '../css/ChatWindow.css';
import { responseInterceptor } from '../utils/ResponseInterceptor';
import { FaFileUpload } from "react-icons/fa";

const ChatWindow = () => {
    const { sessionId, updateSession } = useContext(SessionContext);
    const location = useLocation();
    const navigate = useNavigate();
    const chatRef = useRef(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);

    const isFetching = useRef(false);
    const hasFetched = useRef(false);

    const initialHistory = useRef([]);
    const initialQuery = useRef(location.state?.initialMessage || null);
    const isProcessed = useRef(false);

    useEffect(() => {
        if (hasFetched.current || isFetching.current) return;

        const initChat = async () => {
            isFetching.current = true;
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
                hasFetched.current = true;
            } catch (err) {
                console.error("데이터 로드 실패:", err);
            } finally {
                isFetching.current = false;
                setIsLoaded(true);

                if (location.state?.initialMessage) {
                    navigate(location.pathname, { replace: true, state: {} });
                }
            }
        };
        initChat();
    }, [sessionId, updateSession, navigate, location.pathname, location.state?.initialMessage, isLoaded]);

    const handleFileUpload = async (file) => {

        // TODO[wcw] 파일 업로드 API 호출
        // await chatApi.uploadReport(file);

        setTimeout(() => {
            if (chatRef.current) {
                chatRef.current.submitUserMessage({
                    text: `[파일 업로드 완료]\n ${file.name} 분석을 시작해줘.`,
                });
            } else {
                console.error("파일 업로드 에러");
            }
        }, 300);
    };

    return (
        <div className="container">
            <div className="header">
                <span className="header-title">대국민 챗봇</span>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="report-upload-button"
                >
                    <FaFileUpload />리포트 업로드
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

                            // 렌더링이 완전히 끝난 후 전송
                            setTimeout(() => {
                                chatElement.submitUserMessage({ text: initialQuery.current });
                                initialQuery.current = null; // 전송 후 비움
                            }, 1000);
                        }
                    }}
                    connect={{
                        url: `${process.env.REACT_APP_PUBLIC_API_URL}/public/stream-chat`,
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
                    inputAreaStyle={Styles.inputAreaStyles}
                    submitButtonStyles={Styles.submitButtonStyles}
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