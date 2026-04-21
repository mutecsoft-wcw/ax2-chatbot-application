export const chatApi = {
  // 히스토리 가져오기
  fetchHistory: async (sessionId) => {
    const baseUrl = `${process.env.REACT_APP_PUBLIC_API_URL}/history`;
    const finalUrl = `${baseUrl}?sessionId=${encodeURIComponent(sessionId)}`;
    const response = await fetch(finalUrl);
    if (!response.ok) throw new Error("히스토리 로드 실패");
    return response.json();
  },

  // TODO[wcw] 원본 html 리포트 요청
//   createReport: async (sessionId) => {
//     const baseUrl = process.env.REACT_APP_CREATE_REPORT_URL;
//     const finalUrl = ``;
//     const response = await fetch(finalUrl);
//     if (!response.ok) throw new Error("리포트 생성 실패");
//     return response.json();
//   },

  // TODO[wcw] 원본 html 리포트 파일 전송
//   uploadReport: async (file, sessionId) => {
//     const baseUrl = process.env.REACT_APP_POST_REPORT_URL;
//     const finalUrl = ``;
//     const response = await fetch(finalUrl);
//     if (!response.ok) throw new Error("리포트 전송 실패");
//     return response.json();
//   },

  // TODO[wcw] 설문 데이터 전송 data -> id, label, value
  postSurveyData: async (surveyAnswers, sessionId) => {
    const baseUrl = process.env.REACT_APP_POST_SURVEY_DATA_URL;
    const finalUrl = `${baseUrl}`;
    const response = await fetch(finalUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sessionId: sessionId,
        answer: surveyAnswers,
        timestamp: new Date().toISOString(),
      }),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || "설문 데이터 전송 실패");
    }
    return response.json();
  },

  // TODO[wcw] 설문 데이터 응답값 보기 조회 
  fetchSurveyValue: async (id, value) => {
    const baseUrl = process.env.REACT_APP_SEARCH_SURVEY_VALUE_URL;
    const finalUrl = `${baseUrl}?id=${encodeURIComponent(id)}&value=${encodeURIComponent(value)}`;
    const response = await fetch(finalUrl);
    if (!response.ok) throw new Error("응답값 보기 로드 실패");
    return response;
  },

  // TODO[wcw] 개인 맞춤형 리포트 요청
//   createPesonalReport: async (sessionId) => {
//     const baseUrl = process.env.REACT_APP_CREATE_PERSONAL_REPORT_URL;
//     const finalUrl = ``;
//     const response = await fetch(finalUrl);
//     if (!response.ok) throw new Error("개인 맞춤형 리포트 생성 실패");
//     return response.json();
//   },
};
