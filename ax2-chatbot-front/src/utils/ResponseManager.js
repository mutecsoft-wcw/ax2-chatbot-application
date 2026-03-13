/**
 * ResponseManager: 백엔드 응답을 프론트엔드 UI 스펙으로 변환
 */
export const ResponseManager = {
    processResponse: (response) => {
      // response가 없으면 기본 텍스트 객체 반환
      if (!response) return { text: "" };
  
      const { type, data, text } = response;
      
      // Deep Chat 에러 방지용 기본 텍스트 설정
      const safeText = text || "";
  
      // 단순 텍스트이거나 type이 없는 경우 (스트리밍 중간 조각 포함)
      if (!type || type === "text") {
        return { text: safeText };
      }
  
      // 이미지 다수 건 처리
      if (type === 'images' && Array.isArray(data)) {
        const imagesHtml = `
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px;">
            ${data.map(url => `
              <img 
                src="${url}" 
                onclick="window.openImageModal('${url}'); return false;" 
                style="width: 100%; border-radius: 15px; border: 1px solid #eee; cursor: pointer;" 
              />
            `).join('')}
          </div>`;
        return { text: safeText, html: imagesHtml };
      }
  
      // 동영상 처리
      if (type === "video" && data) {
        const videoHtml = `
          <div class="video-card" style="cursor: pointer; position: relative;" onclick="window.openVideoModal('${data.url}')">
            <img src="${data.thumbnail}" style="width: 100%; border-radius: 10px;" />
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 5px;">▶ 재생하기</div>
          </div>`;
        return { text: safeText || "동영상 가이드를 확인하세요.", html: videoHtml };
      }
  
      // 리포트/파일 처리
      if (type === "report" && data) {
        const fileHtml = `
          <div class="file-card" style="padding: 10px; border: 1px solid #ddd; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 20px;">📄</span>
            <div>
              <strong style="display: block;">${data.name || '리포트'}</strong>
              <a href="${data.url}" download style="color: #003764; font-size: 0.8rem; text-decoration: underline;">다운로드</a>
            </div>
          </div>`;
        return { text: safeText, html: fileHtml };
      }
  
      // 어떤 조건에도 맞지 않으면 최소한 텍스트라도 반환 ({} 에러 방지)
      return { text: safeText };
    },
  };