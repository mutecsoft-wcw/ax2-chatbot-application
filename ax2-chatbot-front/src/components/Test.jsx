import React, { useEffect, useRef } from 'react';
import { DeepChat } from 'deep-chat-react';
import { ResponseManager } from '../utils/ResponseManager';

const Test = () => {
    const chatRef = useRef(null);
    const isInitRender = useRef(true);

    useEffect(() => {
        window.submitChatResponse = (message) => {
            if (chatRef.current) {
                // 사용자가 버튼을 눌렀을 때 해당 텍스트를 채팅창에 전송
                chatRef.current.submitUserMessage({text: message});
            } else {
                console.error("DeepChat ref가 아직 연결되지 않았습니다.");
            }
        };

        // 초기 메시지를 가져오는 비동기 함수
        const fetchInitMessage = async () => {
            if (!isInitRender.current) return;
            isInitRender.current = false;

            // TODO[wcw] 초기 메시지 API 호출
            // 실제 환경에서는: const response = await fetch('url');
            // 초기 메시지 데이터
            const mockInitialMessage = {
                type: "survey_initial_question",
                text: "건강과 관련한 간단한 설문을 기반으로 맞춤 리포트를 받아보시겠습니까?",
                data: {
                    buttons: [
                        { label: "예", value: "예" },
                        { label: "아니오", value: "아니오" }
                    ]
                }
            };

            if (chatRef.current) {
                const processed = ResponseManager.processResponse(mockInitialMessage);
                chatRef.current.addMessage(processed);
            }
        };

        if (chatRef.current) {
            // 초기 메시지 호출
            setTimeout(fetchInitMessage, 500);

            // Demo 모드 설정 (사용자 응답 시뮬레이션)
            chatRef.current.demo = {
                displayLoading: true,
                response: (messageObj) => {
                    const userText = typeof messageObj === 'string' ? messageObj : (messageObj.text || "");

                    if (userText.trim() === "예") {
                        const MockSurveyData = {
                            type: "survey_form",
                            text: "간단 설문", // 설문지 상단 메시지
                            data: {
                                questions: [
                                    { id: "q1", label: "운동 빈도", options: ["주 0회", "주 1-2회", "주 3회 이상"] },
                                    { id: "q2", label: "수면 시간", options: ["5시간 이하", "6-7시간", "8시간 이상"] },
                                    { id: "q3", label: "식습관", options: ["규칙적", "불규칙적"] }
                                ]
                            }
                        };
                        return ResponseManager.processResponse(MockSurveyData);
                    }
                    return { text: "알겠습니다. 도움이 필요하시면 언제든 말씀해주세요." };
                }
            };

            chatRef.current.messageStyles = {
                html: { shared: { bubble: { backgroundColor: 'unset', padding: '0px', width: 'auto' } } }
            };
        }
    }, []);

    return (
        <div style={{ padding: '20px', display: 'flex', justifyContent: 'center' }}>
            <DeepChat
                ref={chatRef}
                style={{ height: '600px', width: '100%', maxWidth: '450px', borderRadius: '15px' }}
                textInput={{ disabled: true, placeholder: { text: '설문을 완료해주세요' } }}
            />
        </div>
    );
};

export default Test;