import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SessionContext } from '../context/SessionContext';
import { chatApi } from '../api/chatApi';
import * as Styles from '../style/ChatStyles';
import FileUploadModal from './modal/FileUploadModal';
import '../css/ChatWindow.css';
import { responseInterceptor } from '../utils/ResponseInterceptor';
import { FaFileUpload } from "react-icons/fa";
import { FaArrowUp } from "react-icons/fa6";

const ChatWindow = () => {
    const { sessionId, updateSession } = useContext(SessionContext);
    const location = useLocation();
    const navigate = useNavigate();
    const chatRef = useRef(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);
    const [isReportReady, setIsReportReady] = useState(false);
    const [isSurveyActive, setIsSurveyActive] = useState(false);
    const [isSurveyVisible, setIsSurveyVisible] = useState(true);

    const isFetching = useRef(false);
    const hasFetched = useRef(false);

    const initialHistory = useRef([]);
    const initialQuery = useRef(location.state?.initialMessage || null);
    const isProcessed = useRef(false);

    const scrollToSurvey = () => {
        if (!chatRef.current) {
            console.warn("chatRef.current가 null입니다.");
            return;
        }

        const chatElement = chatRef.current.children?.[0] || chatRef.current;

        if (chatElement && chatElement.shadowRoot) {
            const surveyElement = chatElement.shadowRoot.getElementById("survey_form")
                || chatElement.shadowRoot.querySelector(".dynamic-survey-card");

            if (surveyElement) {
                surveyElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                console.warn("Shadow Root 내부에서 survey_form을 찾을 수 없습니다.");
            }
        } else {
            const normalElement = document.getElementById("survey_form");
            if (normalElement) {
                normalElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                console.error("DeepChat 컴포넌트 혹은 ShadowRoot를 찾을 수 없습니다.");
                console.log("현재 Ref 상태:", chatRef.current);
            }
        }
    };

    // 사용자 응답을 통해 리포트 업로드 버튼 노출 여부 결정
    const handleMessageResponse = useCallback(() => {
        if (!chatRef.current || typeof chatRef.current.getMessages !== 'function') {
            return;
        }

        const allMessages = chatRef.current.getMessages();
        if (allMessages.length < 2) return;

        const hasSurvey = allMessages.some(msg =>
            (msg.html || "").includes("dynamic-survey-card")
        );
        setIsSurveyActive(hasSurvey);

        let isMatched = false;

        for (let i = allMessages.length - 1; i >= 1; i--) {
            const currentUserMsg = allMessages[i];
            const prevAiMsg = allMessages[i - 1];

            if (currentUserMsg.role === 'user') {
                const userText = (currentUserMsg.text || "").trim();
                const aiText = (prevAiMsg.html || prevAiMsg.text || "").replace(/<[^>]*>?/gm, '');

                const positiveWords = ["예", "응", "네", "그래", "__START_SURVEY__", "좋아"];
                const isUserPositive = positiveWords.some(word => userText.includes(word));
                const isAiAsking = aiText.includes("간단 설문을 진행하시겠습니까?");

                // 사용자가 긍정했고, 바로 전 메시지가 AI의 특정 질문일 때
                if (isUserPositive && isAiAsking) {
                    isMatched = true;
                    break; // 가장 최근 쌍만 확인하고 종료
                }
            }
        }

        setIsReportReady(prev => {
            // 현재 상태와 새로 판단된 결과가 다를 때만 업데이트 (새로고침 현상 방지)
            if (prev !== isMatched) return isMatched;
            return prev;
        });
    }, []);

    useEffect(() => {
        if (hasFetched.current || isFetching.current) return;

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

    // 설문 예, 아니오 버튼 응답 처리 로직
    useEffect(() => {
        window.handleChatAction = (action, sessionId) => {

            if (action === "START_SURVEY") {
                chatRef.current?.submitUserMessage({
                    text: "__START_SURVEY__",
                    role: "user"
                });
            }

            if (action === "CANCEL_SURVEY") {
                chatRef.current?.submitUserMessage({
                    text: "__CANCEL_SURVEY__",
                    role: "user"
                });
            }
        };

        return () => {
            delete window.handleChatAction;
        };
    }, [sessionId, navigate]);

    // useEffect(() => {
    //     if (!isSurveyActive) return;
    
    //     const timer = setTimeout(() => {
    //         const chatElement = document.querySelector('deep-chat');
    //         const shadow = chatElement?.shadowRoot;
    //         console.log(shadow);
    //         const messageList = shadow?.getElementById("messages");
    //         const survey = shadow?.getElementById("survey_form") || shadow?.querySelector(".dynamic-survey-card");
    
    //         if (!messageList || !survey) return;
    
    //         const observer = new IntersectionObserver(
    //             ([entry]) => {
    //                 const isVisible = entry.isIntersecting;
    //                 setIsSurveyVisible(isVisible);
                    
    //                 // 설문지가 보이면 스크롤바 숨김, 안 보이면 노출
    //                 messageList.style.overflowY = isVisible ? 'hidden' : 'auto';
                    
    //                 if (isVisible) {
    //                     const style = document.createElement('style');
    //                     style.id = "hide-scroll-css";
    //                     style.innerHTML = `#message-list::-webkit-scrollbar { display: none; }`;
    //                     shadow.appendChild(style);
    //                 } else {
    //                     shadow.getElementById("hide-scroll-css")?.remove();
    //                 }
    //             },
    //             { threshold: 0.5 } // 50% 이상 보일 때 기준
    //         );
    
    //         observer.observe(survey);
    //         return () => observer.disconnect();
    //     }, 500); 
    
    //     return () => clearTimeout(timer);
    // }, [isSurveyActive]);

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

    const memoizedChat = useMemo(() => (
        <DeepChat
            ref={chatRef}
            style={Styles.chatComponentStyle}
            history={initialHistory.current}
            stream={true}
            scrollButton={Styles.scrollBtnStyles}
            onMessage={() => {
                setTimeout(() => handleMessageResponse(), 100);
            }}
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
    ), [isLoaded, handleMessageResponse]);

    return (
        <div className="container">
            <div className="header">
                <span className="header-title">무엇이든 물어보세요, 건강지기</span>
                {isReportReady && (
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="report-upload-button"
                    >
                        <span><FaFileUpload />리포트 업로드</span>
                    </button>
                )}
            </div>

            {isLoaded ? memoizedChat : (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <p>대화 내용을 불러오는 중입니다...</p>
                </div>
            )}

            {isSurveyActive && (
                <div className='floating-survey-scroll-btn-wrap'>
                    <button className='floating-survey-scroll-btn' onClick={() => scrollToSurvey()}>설문지로 이동 <FaArrowUp /></button>
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