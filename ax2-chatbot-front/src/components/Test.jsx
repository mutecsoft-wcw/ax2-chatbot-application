import React, { useContext, useEffect, useRef } from 'react';
import { DeepChat } from 'deep-chat-react';
import { ResponseManager } from '../utils/ResponseManager';
import * as Styles from '../style/ChatStyles';
import '../css/ChatWindow.css';
import { chatApi } from '../api/chatApi';
import { SessionContext } from '../context/SessionContext';


const Test = () => {
    const chatRef = useRef(null);
    const { sessionId } = useContext(SessionContext);
    window.sessionId = sessionId;


    useEffect(() => {
        window.MockSurveyData = {
            type: "survey_form",
            text: "간단 설문",
            data: {
                questions: [
                    { id: "q1", label: "운동 빈도", options: ["주 0회", "주 1-2회", "주 3회 이상"] },
                    { id: "q2", label: "수면 시간", options: ["5시간 이하", "6-7시간", "8시간 이상"] },
                    { id: "q3", label: "식습관", options: ["규칙적", "불규칙적"] }
                ]
            }
        };

        window.submitChatResponse = (message) => {
            if (chatRef.current) chatRef.current.submitUserMessage({ text: message });
        };

        window.submitSurvey = async (buttonElement) => {
            const surveyContainer = buttonElement.closest('.dynamic-survey-card');

            if (!surveyContainer) {
                console.error("설문을 찾을 수 없습니다. HTML 구조를 확인하세요.");
                return;
            }

            const questions = window.MockSurveyData?.data?.questions || [];

            const surveyResults = questions.map(q => {
                const selectElement = surveyContainer.querySelector(`#${q.id}`);
                return {
                    id: q.id,
                    label: q.label,
                    value: selectElement ? selectElement.value : "미응답"
                };
            });

            console.log("전송할 데이터 SessionId: ", window.sessionId);
            console.log("전송할 데이터 SurveyResults: ", surveyResults);

            try {
                await chatApi.postSurveyData(surveyResults, window.sessionId);
                if (chatRef.current) {
                    chatRef.current.addMessage({ text: "설문이 완료되었습니다!", role: "ai" });
                }
            } catch (error) {
                alert("전송 실패");
            }
        };

        if (chatRef.current) {
            chatRef.current.demo = {
                displayLoading: true,
                response: (messageObj) => {
                    const userText = typeof messageObj === 'string' ? messageObj : (messageObj.text || "");

                    if (userText.includes("리포트") || userText.includes("만들어줘")) {
                        return { text: "네, 원본 리포트를 업로드 해주세요." };
                    }

                    if (userText.trim() === "예") {
                        return ResponseManager.processResponse(window.MockSurveyData);
                    }
                    return { text: "도움이 필요하시면 말씀해주세요." };
                }
            };
        }

        // 클린업 시 전역 변수 삭제
        return () => {
            delete window.submitSurvey;
            delete window.submitChatResponse;
            delete window.MockSurveyData;
        };
    }, [sessionId]);

    // 파일 업로드 시 호출될 함수
    const handleFileUpload = (file) => {
        if (chatRef.current) {
            // 파일 업로드 완료 알림
            chatRef.current.addMessage({
                text: `[파일 업로드 완료]\n${file.name} 분석을 시작하기 위해 몇 가지 질문을 드려도 될까요?`,
                role: "ai"
            });

            // '예/아니오' 버튼 메시지 추가 (의사 확인)
            const MockAskSurvey = ResponseManager.processResponse({
                type: "survey_initial_question",
                text: "맞춤 리포트를 위해 간단한 설문에 참여하시겠습니까?",
                data: {
                    buttons: [
                        { label: "예", value: "예" },
                        { label: "아니오", value: "아니오" }
                    ]
                }
            });
            chatRef.current.addMessage(MockAskSurvey);
        }
    };

    return (
        <div className='container'>
            <div className='header'>
                <span className="header-title">테스트 챗봇</span>
                <button
                    onClick={() => handleFileUpload({ name: 'test.html' })}
                    className='report-upload-button'
                >
                    (테스트용) 리포트 업로드
                </button>
            </div>

            <DeepChat
                ref={chatRef}
                style={Styles.chatComponentStyle}
                textInput={Styles.textInputStyle}
                submitButtonStyles={Styles.submitButtonStyles}
            />
        </div>
    );
};

export default Test;