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

    return { text: safeText };
  },
};
