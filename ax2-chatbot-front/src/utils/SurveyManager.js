export const SurveyManager = {
  styles: `
        <style>
            .health-survey-card {
                width: 95%; 
                max-width: 600px; 
                margin: 10px auto; 
                border: 1px solid #333;
                background: #fff;
                font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                color: #000;
                padding: 20px;
                box-sizing: border-box;
                line-height: 1.5;
                word-break: keep-all;
            }
            .main-header-section {
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 4px double #2c3e50; /* 공공기관 특유의 이중선 */
                padding-bottom: 20px;
                position: relative;
            }
            .main-header-title {
                font-size: clamp(20px, 5vw, 28px);
                font-weight: 900;
                color: #1a2a3a;
                letter-spacing: clamp(2px, 1.5vw, 6px); /* 글자 사이를 벌려 권위 있는 느낌 강조 */
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
            .question-text { 
                display: flex;         
                align-items: flex-start; 
                font-weight: bold;
                margin-bottom: 12px;
                font-size: 15px;
                line-height: 1.4; 
            }
            .question-text .num {
                min-width: 28px;        /* 번호가 차지할 최소 공간 고정 */
                margin-right: 4px;      /* 번호와 질문 사이 간격 */
                flex-shrink: 0;         /* 번호 영역이 찌그러지지 않게 설정 */
                color: #2c3e50;
            }
            .question-content {
                flex: 1;                /* 남은 공간을 모두 차지 */
                word-break: keep-all;    /* 한글 단어가 어색하게 깨지지 않게 함 */
            }

            /* 입력 행 스타일 */
            .input-row { margin-left: 24px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
            
            .gov-input {
                flex: 1 1 auto; /* 너비가 유연하게 변함 */
                min-width: 50px;
                max-width: 30%;
                padding: 8px;
                border: 1px solid #777;
                border-radius: 2px;
                font-size: 14px;
                box-sizing: border-box;
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

            /* --- 페이지네이션 관련 새 스타일 --- */
            .survey-section { display: none; } /* 기본적으로 숨김 */
            .survey-section.active { display: block; } /* 현재 페이지 때만 표시 */

            .btn-group {
                margin-top: 30px;
                border-top: 1px solid #eee;
                padding-top: 20px;
                display: flex;
                gap: 10px;
                justify-content: center; /* 버튼 중앙 정렬 */
            }

            .gov-btn {
                padding: 10px 20px;
                border: 1px solid #777;
                border-radius: 2px;
                font-weight: bold;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.2s;
            }

            /* 이전 버튼 (흰색 배경) */
            .btn-prev { background: #fff; color: #333; }
            .btn-prev:hover { background: #f5f5f5; }

            /* 다음/제출 버튼 (정부색 배경) */
            .btn-next, .btn-submit { background: #2c3e50; color: white; border: none; }
            .btn-next:hover, .btn-submit:hover { background: #1a2a3a; }
        </style>
    `,

  renderQuestion: (q, index) => {
    const questionNum = `<span class="num">${index + 1}.</span>`;

    if (q.type === "text") {
      return `
          <div class="question-item">
            <div class="question-text">
              <span class="num">${index + 1}.</span> 
              <div class="question-content">${q.question}</div>
            </div>
            <div class="input-row">
              <input class="gov-input" placeholder="${q.placeholder}" />
              ${q.suffix || ""}
            </div>
          </div>
        `;
    }

    if (q.type === "number") {
      return `
          <div class="question-item">
            <div class="question-text">
              <span class="num">${index + 1}.</span>
              <div class="question-content">${q.question}</div>
            </div>
            <div class="input-row">
              <input type="number" class="gov-input" style="width:60px;" placeholder="${
                q.placeholder
              }" min="${q.min}" max="${q.max}"/>
              ${q.suffix || ""}
            </div>
          </div>
        `;
    }

    if (q.type === "radio") {
      return `
            <div class="question-item">
              <div class="question-text">
                <span class="num">${index + 1}.</span>
                <div class="question-content">${q.question}</div>
              </div>
              <div class="input-row">
                ${q.options
                  .map(
                    (opt) => `
                  <label style="display: flex; align-items: center; gap: 4px; cursor: pointer; margin-right: 15px;">
                    <input type="radio" name="${q.id}" value="${opt.value}"/>
                    <span>${opt.label}</span>
                  </label>
                `
                  )
                  .join("")}
              </div>
            </div>
          `;
    }

    if (q.type === "select") {
      return `
          <div class="question-item">
            <div class="question-text">
              <span class="num">${index + 1}.</span>
              <div class="question-content">${q.question}</div>
            </div>
            <div class="input-row">
              <select class="gov-select" style="width:180px;">
                <option value="">선택</option>
                ${q.options
                  .map(
                    (opt) => `
                  <option value="${opt.value}">${opt.label}</option>
                `
                  )
                  .join("")}
              </select>
            </div>
          </div>
        `;
    }

    if (q.type === "composite") {
      const inputsHtml = q.units
        .map(
          (u) => `
          <div style="display: flex; align-items: center; gap: 5px; margin-right: 15px;">
            <input type="number" 
                   class="gov-input" 
                   id="${u.id}" 
                   style="width:60px;" 
                   placeholder="${u.placeholder || ""}" />
            <span class="unit">${u.label}</span>
          </div>
        `
        )
        .join("");

      return `
          <div class="question-item">
            <div class="question-text">
                <span class="num">${questionNum}</span>
            <div class="question-content">${q.question}</div>
            </div>
            <div class="input-row" style="display: flex; flex-wrap: wrap;">
              ${inputsHtml}
            </div>
          </div>
        `;
    }

    return "";
  },

  generateSurveyHtml: (data) => {
    const surveyId = `survey_${Date.now()}`;
    const totalSections = data.sections.length;

    const sectionsHtml = data.sections
      .map((section, sIndex) => {
        const isFirst = sIndex === 0;
        const isLast = sIndex === totalSections - 1;

        let buttonsHtml = '<div class="btn-group">';
        if (totalSections > 1) {
          if (!isFirst) {
            buttonsHtml += `<button type="button" class="gov-btn btn-prev" onclick="surveyControl.changePage(this, ${
              sIndex - 1
            })">이전</button>`;
          }
          if (!isLast) {
            buttonsHtml += `<button type="button" class="gov-btn btn-next" onclick="surveyControl.changePage(this, ${
              sIndex + 1
            })">다음</button>`;
          }
        }
        if (isLast) {
          buttonsHtml += `<button type="button" class="gov-btn btn-submit" onclick="surveyControl.submit(this)">설문 제출</button>`;
        }
        buttonsHtml += "</div>";

        return `
          <div id="section_${sIndex}" class="survey-section ${
          isFirst ? "active" : ""
        }">
            <div class="health-main-title">${section.title}</div>
            ${section.questions
              .map((q, i) => SurveyManager.renderQuestion(q, i))
              .join("")}
            ${buttonsHtml}
          </div>`;
      })
      .join("");

    return {
      html: `
        ${SurveyManager.styles}
        <div id="${surveyId}" class="dynamic-survey-card health-survey-card">
          <div class="main-header-section">
            <h1 class="main-header-title">${data.title}</h1>
            <div class="main-header-subtitle">${data.subtitle}</div>
          </div>
          ${sectionsHtml}
        </div>`,
    };
  },
};

export const surveyControl = {
  // 페이지 전환 로직
  changePage: (btn, targetIndex) => {
    const surveyCard = btn.closest(".health-survey-card");

    const sections = surveyCard.querySelectorAll(".survey-section");
    sections.forEach((s) => s.classList.remove("active"));

    const targetSection = surveyCard.querySelector(`#section_${targetIndex}`);
    if (targetSection) {
      targetSection.classList.add("active");
    }

    surveyCard.scrollIntoView({ behavior: "smooth", block: "start" });
  },

  // 제출 로직
  submit: (btn) => {
    const surveyCard = btn.closest(".health-survey-card");
    const inputs = surveyCard.querySelectorAll("input, select");

    const results = {};
    inputs.forEach((input) => {
      if (input.type === "radio") {
        if (input.checked) results[input.name] = input.value;
      } else {
        results[input.id || input.name] = input.value;
      }
    });

    console.log("설문 제출 데이터:", results);
    alert("설문이 제출되었습니다. 콘솔을 확인하세요!");

    // TODO[wcw] 서버 전송 로직 혹은 채팅창에 메시지 표시 등
  },
};

if (typeof window !== "undefined") {
  window.surveyControl = surveyControl;
}
