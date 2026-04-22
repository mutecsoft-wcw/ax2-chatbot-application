export const ResponseManager = {
  processResponse: (response) => {
    if (!response) return { text: "" };

    const { type, data, text } = response;
    const safeText = text || "";

    // 단순 텍스트
    if (!type || type === "text") {
      return { text: safeText };
    }

    // 이미지 다수 건 (Grid 레이아웃)
    if (type === "images" && Array.isArray(data)) {
      const imagesHtml = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-top: 10px;">
                    ${data
                      .map(
                        (url) => `
                        <img 
                            src="${url}" 
                            onclick="window.openImageModal('${url}'); return false;" 
                            style="width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 12px; border: 1px solid #eee; cursor: pointer;" 
                        />
                    `
                      )
                      .join("")}
                </div>`;
      return { text: safeText, html: imagesHtml };
    }

    // 동영상 (썸네일 + 재생 아이콘)
    if (type === "video" && data) {
      const videoHtml = `
                <div style="position: relative; cursor: pointer; margin-top: 10px; border-radius: 12px; overflow: hidden;" 
                     onclick="window.openVideoModal('${data.url}')">
                    <img src="${data.thumbnail}" style="width: 100%; display: block;" />
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; background: rgba(0,0,0,0.3);">
                        <div style="width: 40px; height: 40px; background: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; padding-left: 3px;">
                            <span style="color: #003764; font-size: 18px;">▶</span>
                        </div>
                    </div>
                </div>`;
      return { text: safeText || "동영상을 확인해 보세요.", html: videoHtml };
    }

    // 리포트/파일 다운로드
    if (type === "report" && data) {
      const fileHtml = `
                <div style="padding: 12px; border: 1px solid #e9ecef; border-radius: 12px; display: flex; align-items: center; gap: 12px; background: #f8f9fa; margin-top: 10px;">
                    <span style="font-size: 24px;">📄</span>
                    <div style="overflow: hidden;">
                        <strong style="display: block; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${
                          data.name || "파일"
                        }</strong>
                        <a href="${
                          data.url
                        }" download style="color: #003764; font-size: 0.8rem; font-weight: bold; text-decoration: none;">다운로드</a>
                    </div>
                </div>`;
      return { text: safeText, html: fileHtml };
    }

    // 간단 설문
    // TODO[wcw]  window.submitChatResponse(results); -> 설문 응답 데이터 전송 api로 변경
    if (type === "survey_form" && data?.questions) {
      const questionHtml = data.questions
        .map(
          (q) => `
            <div style="margin-bottom: 12px; text-align: left;">
              <label style="font-size: 12px; display: block; color: #666; margin-bottom: 4px;">${
                q.label
              }</label>
              <select id="${
                q.id
              }" class="survey-select" style="width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #ddd; font-size: 14px;">
                ${q.options
                  .map((opt) => `<option value="${opt}">${opt}</option>`)
                  .join("")}
              </select>
            </div>`
        )
        .join("");

      return {
        html: `
            <div class="dynamic-survey-card" style="background: #fff; padding: 15px; border-radius: 15px; border: 1px solid #eee; box-shadow: 0 4px 6px rgba(0,0,0,0.05); width: 220px;">
              <p style="font-weight: bold; margin-bottom: 15px; font-size: 15px;">${safeText}</p>
              ${questionHtml}
              <button onclick="window.submitSurvey(this)" 
                        style="width: 100%; background: #003764; color: white; border: none; padding: 10px; border-radius: 20px; font-weight: bold; cursor: pointer; margin-top: 5px;">
                    설문 완료
                </button>
            </div>`,
        role: "ai",
      };
    }

    // TODO[wcw]  window.submitChatResponse(results); -> 설문 응답 데이터 전송 api로 변경
    if (type === "survey_initial_question") {
      const buttonsHtml = data.buttons
        .map(
          (btn) => `
          <button onclick="window.submitChatResponse('${btn.value}')" 
                  style="background: ${"var(--gok-blue)"}; 
                         color: ${"white"}; 
                         border: none; padding: 5px 15px; border-radius: 15px; cursor: pointer;">
            ${btn.label}  
          </button>
        `
        )
        .join("");

      return {
        text: safeText,
        html: `<div style="display: flex; gap: 8px; margin-top: 10px;">${buttonsHtml}</div>`,
        role: "ai",
      };
    }

    if (type === "survey_question") {
      const questionHtml = `
        <p margin-bottom: 10px;">
          ${data.text || ""}
        </p>
      `;
      const buttonsHtml = data.buttons
        .map(
          (btn) => `
        <button 
          onclick='window.handleChatAction("${btn.action}", ${JSON.stringify(
            btn.payload || {}
          )})'
          style="background: var(--gok-blue); 
                color: white; 
                border: none; padding: 5px 15px; border-radius: 15px; cursor: pointer;">
          ${btn.label}
        </button>
      `
        )
        .join("");

      return {
        role: "ai",
        html: `
          ${questionHtml}
          <div style="display: flex; gap: 8px; margin-top: 10px;">
            ${buttonsHtml}
          </div>
        `,
      };
    }

    if (type === "custom_html") {
      const surveyId = `survey_${Date.now()}`; // TODO[wcw] 임시 설문ID값 내용 공유 후 의견 종합 필요.

      const surveyStyles = `
        <style>
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
      `;

      const renderQuestion = (q, index) => {
        if (q.type === "text") {
          return `
            <div class="question-item">
              <div class="question-text">
                <span class="num">${index + 1}.</span> ${q.question}
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
                <span class="num">${index + 1}.</span> ${q.question}
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
                  <span class="num">${index + 1}.</span> ${q.question}
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
                <span class="num">${index + 1}.</span> ${q.question}
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

        return "";
      };

      const totalSections = data.sections.length;

      const sectionsHtml = data.sections
        .map((section, sIndex) => {
          const isFirst = sIndex === 0;
          const isLast = sIndex === totalSections - 1;

          let buttonsHtml = '<div class="btn-group">';

          if (totalSections > 1) {
            // 페이지가 여러 개일 때만 네비게이션 버튼 표시
            if (!isFirst) {
              // 첫 페이지가 아니면 '이전' 버튼 추가
              buttonsHtml += `
          <button type="button" class="gov-btn btn-prev" 
            onclick="
              const card = this.closest('.health-survey-card');
              card.querySelectorAll('.survey-section').forEach(s => s.classList.remove('active'));
              card.querySelector('#section_${
                sIndex - 1
              }').classList.add('active');
            ">이전 페이지로</button>`;
            }

            if (!isLast) {
              // 마지막 페이지가 아니면 '다음' 버튼 추가
              buttonsHtml += `
          <button type="button" class="gov-btn btn-next" 
            onclick="
              const card = this.closest('.health-survey-card');
              card.querySelectorAll('.survey-section').forEach(s => s.classList.remove('active'));
              card.querySelector('#section_${
                sIndex + 1
              }').classList.add('active');
            ">다음 페이지로</button>`;
            }
          }

          if (isLast) {
            // 마지막 페이지라면 '제출' 버튼 추가
            buttonsHtml += `
        <button type="button" class="gov-btn btn-submit" 
          onclick="
            const card = this.closest('.health-survey-card');
            const data = {};
            card.querySelectorAll('input, select').forEach(i => {
              if(i.type === 'radio' && !i.checked) return;
              if(i.name || i.id) data[i.name || i.id] = i.value;
            });
            console.log('제출 데이터:', data);
            alert('설문 제출 완료! 콘솔을 확인하세요.');
          ">설문 제출</button>`;
          }

          buttonsHtml += "</div>";

          return `
            <div id="section_${sIndex}" class="survey-section ${
                    isFirst ? "active" : ""
                }">
                <div class="health-main-title">${section.title}</div>
                ${section.questions.map((q, i) => renderQuestion(q, i)).join("")}
                ${buttonsHtml}
            </div>
            `;
        })
        .join("");

      return {
        role: "ai",
        html: `
              ${surveyStyles}
              <div id="${surveyId}" class="dynamic-survey-card health-survey-card">
                <div class="main-header-section">
                  <h1 class="main-header-title">${data.title}</h1>
                  <div class="main-header-subtitle">${data.subtitle}</div>
                </div>
                ${sectionsHtml}
              </div>
            `,
      };
    }

    return { text: safeText };
  },
};
