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
        window.changePage = (hidePageId, showPageId) => {
            const hideElement = document.getElementById(hidePageId);
            const showElement = document.getElementById(showPageId);
            
            if (hideElement && showElement) {
                hideElement.style.display = 'none'; // 현재 페이지 숨기기
                showElement.style.display = 'block'; // 다음 페이지 보여주기
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
            delete window.changePage;
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
                history={[{ html: surveyHtml, role: "ai" }]}
            />
        </div>
    );
};

const surveyStyles = `
    .health-survey-card {
        width: 100%; min-width: 600px; max-width: 600px; border: 1px solid #333;
        background: #fff; font-family: 'Malgun Gothic', sans-serif; color: #000;
        padding: 20px; box-sizing: border-box; line-height: 1.5;
    }
    .main-header-section {
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 4px double #2c3e50; /* 공공기관 특유의 이중선 */
        padding-bottom: 20px;
        position: relative;
    }
    .main-header-title {
        font-size: 28px;
        font-weight: 900;
        color: #1a2a3a;
        letter-spacing: 6px; /* 글자 사이를 벌려 권위 있는 느낌 강조 */
        margin: 10px 0;
        padding-left: 6px; /* letter-spacing으로 인한 비대칭 교정 */
    }
    .main-header-subtitle {
        font-size: 13px;
        color: #555;
        font-weight: bold;
        background: #f0f0f0;
        display: inline-block;
        padding: 2px 15px;
        border-radius: 15px;
    }
    .health-main-title {
        font-size: 20px; font-weight: bold; border-bottom: 2px solid #000;
        padding-bottom: 5px; margin-bottom: 20px; display: inline-block;
    }
    /* 안내 문구 박스 */
    .info-box {
        background-color: #f1f4f8; border: 1px solid #d1d5db;
        padding: 10px 12px; margin-bottom: 15px; font-size: 13px; font-weight: bold;
        color: #2c3e50;
    }
    
    .question-item { margin-bottom: 22px; font-size: 14px; }
    .question-text { font-weight: bold; margin-bottom: 10px; }
    .question-text .num { margin-right: 8px; font-size: 15px; }

    /* 입력 행 스타일 */
    .input-row { margin-left: 24px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
    
    .gov-input {
        padding: 5px 8px; border: 1px solid #777; border-radius: 2px;
        font-size: 14px; outline: none;
    }
    .gov-input:focus { border-color: #2c3e50; background: #f9f9f9; }
    
    .gov-select {
        padding: 5px; border: 1px solid #777; border-radius: 2px;
        font-size: 14px; background: #fff;
    }

    /* 하위 질문 (ㄴ 화살표) */
    .sub-question { margin-left: 28px; margin-top: 12px; position: relative; }
    .sub-question::before { 
        content: '└'; position: absolute; left: -18px; top: 0; 
        font-weight: bold; color: #2c3e50; 
    }

    .unit { font-size: 13px; color: #333; margin-left: 2px; }

    /* 버튼 스타일 */
    .gov-footer { margin-top: 30px; border-top: 1px solid #000; padding-top: 20px; }
    .gov-btn-submit {
        width: 100%; padding: 12px; background: #2c3e50; color: white;
        border: none; border-radius: 2px; font-weight: bold; cursor: pointer; font-size: 15px;
    }
    .gov-btn-submit:hover { background: #1a2a3a; }
`;

const surveyHtml = `
    <style>${surveyStyles}</style>
    <div class="dynamic-survey-card health-survey-card">
      <div class="main-header-section">
          <h1 class="main-header-title">대국민 간단 설문지</h1>
          <div class="main-header-subtitle">생활 패턴 및 기초 건강 실태조사</div>
      </div>
      
      <div id="survey-page-1" style="display: block;">
          <div class="health-main-title">인적사항 (1/2)</div>
            
          <div class="question-item">
            <div class="question-text"><span class="num">1.</span> 귀하의 성명과 연령은 어떻게 되십니까?</div>
            <div class="input-row">
              성명: <input type="text" id="name" class="gov-input" style="width:100px;" placeholder="성함">
              / 연령: <input type="number" id="age" class="gov-input" style="width:60px;" min="1"> <span class="unit">세</span>
            </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">2.</span> 귀하의 성별을 선택해 주십시오.</div>
            <div class="input-row">
              <input type="radio" id="sex_male" name="sex" value="남성"> <label for="sex_male">남성</label>
              <input type="radio" id="sex_female" name="sex" value="여성" style="margin-left:15px;"> <label for="sex_female">여성</label>
            </div>
          </div>

          <div class="question-item">
              <div class="question-text"><span class="num">3.</span> 현재 거주하고 계신 지역은 어디입니까?</div>
              <div class="input-row">
                  <select id="residence" class="gov-select" style="width:180px;">
                      <option value="">지역 선택</option>
                      <option value="서울">서울특별시</option><option value="부산">부산광역시</option>
                      <option value="경기">경기도</option><option value="강원">강원도</option>
                  </select>
              </div>
          </div>
                
          <div class="question-item">
              <div class="question-text"><span class="num">4.</span> 현재 종사하고 계신 직업군은 무엇입니까?</div>
              <div class="input-row">
                <select id="job" class="gov-select" style="width:220px;">
                  <option value="">직업군 선택</option>
                  <option value="사무직">사무종사자</option><option value="전문직">전문가 및 관련종사자</option>
                  <option value="서비스">서비스종사자</option><option value="군인">직업군인</option>
                </select>
              </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">5.</span> 귀하의 현재 신장(키)과 체중(몸무게)은 얼마입니까?</div>
            <div class="input-row">
              신장: <input type="number" id="height" class="gov-input" style="width:70px;"> <span class="unit">cm</span>
              / 체중: <input type="number" id="weight" class="gov-input" style="width:70px;" step="0.1"> <span class="unit">kg</span>
            </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">6.</span> 귀하의 혼인 상태를 선택해 주십시오.</div>
            <div class="input-row">
              <select id="marital_status" class="gov-select" style="width:150px;">
                  <option value="">선택해주세요</option>
                  <option value="미혼">미혼</option>
                  <option value="기혼">기혼</option>
                  <option value="기타">기타(이혼/사별)</option>
              </select>
            </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">7.</span> 현재 담배를 피우십니까? (흡연 여부)</div>
            <div class="input-row">
              <input type="radio" id="smoking_yes" name="smoking" value="흡연"> <label for="smoking_yes">흡연</label>
              <input type="radio" id="smoking_no" name="smoking" value="비흡연" style="margin-left:15px;"> <label for="smoking_no">비흡연</label>
            </div>
          </div>

          <div class="gov-footer">
            <button type="button" onclick="const card = this.closest('.dynamic-survey-card'); card.querySelector('#survey-page-1').style.display='none'; card.querySelector('#survey-page-2').style.display='block';" class="gov-btn-submit" style="background-color: #4a5568;">
              다음 페이지로 (1/2) 👉
            </button>
          </div>
      </div>

      <div id="survey-page-2" style="display: none;">
          <div class="health-main-title" style="margin-top:0;">신체활동 (2/2)</div>
            
          <div class="question-item">
            <div class="question-text"><span class="num">1.</span> 최근 1주일 동안 평소보다 몸이 매우 힘들고 숨이 많이 가쁜 고강도 신체활동을 10분 이상 했던 날은 며칠입니까?</div>
            <div class="input-row">
              일주일에 <input type="number" id="q1_days" class="gov-num-input" min="0" max="7" style="width:40px; border:1px solid #777;"> 일
              <span class="guide-text" style="font-size:12px; color:#666; margin-left:10px;">(→ 0일은 2번 문항으로)</span>
            </div>

            <div class="sub-question" style="margin-left:28px; margin-top:10px; position:relative;">
                <div class="question-text" style="font-weight:bold;"><span class="num">1-1.</span> 이러한 고강도 신체활동을 한 날, 보통 하루에 몇 분간 했습니까?</div>
                <div class="input-row">
                  하루에 <input type="number" id="q1_hours" class="gov-num-input" style="width:40px; border:1px solid #777;"> 시간 <input type="number" id="q1_mins" class="gov-num-input" style="width:40px; border:1px solid #777;"> 분
                </div>
            </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">2.</span> 최근 1주일 동안 평소보다 몸이 조금 힘들고 숨이 약간 가쁜 중강도 신체활동을 10분 이상 했던 날은 며칠입니까?</div>
            <div class="input-row">
              일주일에 <input type="number" id="q2_days" class="gov-num-input" min="0" max="7" style="width:40px; border:1px solid #777;"> 일
              <span class="guide-text" style="font-size:12px; color:#666; margin-left:10px;">(→ 0일은 3번 문항으로)</span>
            </div>

            <div class="sub-question" style="margin-left:28px; margin-top:10px; position:relative;">
              <div class="question-text" style="font-weight:bold;"><span class="num">2-1.</span> 이러한 중강도 신체활동을 한 날, 보통 하루에 몇 분간 했습니까?</div>
              <div class="input-row">
                하루에 <input type="number" id="q2_hours" class="gov-num-input" style="width:40px; border:1px solid #777;"> 시간 <input type="number" id="q2_mins" class="gov-num-input" style="width:40px; border:1px solid #777;"> 분
              </div>
            </div>
          </div>
            
          <div class="question-item">
            <div class="question-text"><span class="num">3.</span> 최근 1주일 동안 한 번에 적어도 10분 이상 걸었던 날은 며칠입니까?</div>
            <div class="input-row">
              일주일에 <input type="number" id="q3_days" class="gov-num-input" min="0" max="7" style="width:40px; border:1px solid #777;"> 일
              <span class="guide-text" style="font-size:12px; color:#666; margin-left:10px;">(→ 0일은 4번 문항으로)</span>
            </div>

            <div class="sub-question" style="margin-left:28px; margin-top:10px; position:relative;">
              <div class="question-text" style="font-weight:bold;"><span class="num">3-1.</span> 이러한 걷기를 한 날, 보통 하루에 몇 분간 했습니까?</div>
              <div class="input-row">
                하루에 <input type="number" id="q3_hours" class="gov-num-input" style="width:40px; border:1px solid #777;"> 시간 <input type="number" id="q3_mins" class="gov-num-input" style="width:40px; border:1px solid #777;"> 분
              </div>
            </div>
          </div>

          <div class="question-item">
            <div class="question-text"><span class="num">4.</span> 최근 1주일 동안 스트레칭, 맨손체조 등의 유연성 운동을 한 날은 며칠입니까?</div>
            <ul class="radio-list" style="list-style:none; padding-left:20px;">
              <li><input type="radio" name="q4" id="q4_1" value="0"> <label for="q4_1">전혀 하지 않음</label></li>
              <li><input type="radio" name="q4" id="q4_2" value="1"> <label for="q4_2">1일</label></li>
              <li><input type="radio" name="q4" id="q4_3" value="2"> <label for="q4_3">2일</label></li>
              <li><input type="radio" name="q4" id="q4_4" value="3"> <label for="q4_4">3일</label></li>
              <li><input type="radio" name="q4" id="q4_5" value="4"> <label for="q4_5">4일</label></li>
              <li><input type="radio" name="q4" id="q4_6" value="5"> <label for="q4_6">5일 이상</label></li>
            </ul>
          </div>

          <div class="gov-footer" style="display: flex; gap: 10px;">
            <button type="button" onclick="const card = this.closest('.dynamic-survey-card'); card.querySelector('#survey-page-2').style.display='none'; card.querySelector('#survey-page-1').style.display='block';" class="gov-btn-submit" style="background-color: #718096; flex: 1;">
              👈 이전
            </button>
            <button type="button" onclick="window.submitSurvey(this)" class="gov-btn-submit" style="flex: 2;">
              설문지 제출하기
            </button>
          </div>
      </div>
    </div>
  `;

export default Test;