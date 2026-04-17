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

    return { text: safeText };
  },
};
