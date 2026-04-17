export const chatApi = {

  // 히스토리 가져오기 
  fetchHistory: async (sessionId) => {
    const baseUrl = `${process.env.REACT_APP_INTERNAL_API_URL}/history`;
    const finalUrl = `${baseUrl}?sessionId=${encodeURIComponent(sessionId)}`;
    const response = await fetch(finalUrl);
    if (!response.ok) throw new Error("히스토리 로드 실패");
    return response.json();
  },
};
