import { ResponseManager } from "./ResponseManager";

export const responseInterceptor = (response) => {
  // 스트리밍 텍스트 처리 (문자열인 경우)
  if (typeof response === "string") {
    const clean = response.replace(/^data:\s*/, "").trim();
    if (!clean || clean === "[DONE]") return null;

    try {
      const parsed = JSON.parse(clean);

      // 만약 최종 응답(이미지/비디오 포함) 구조라면 Manager를 통해 HTML 생성
      if (parsed.type && parsed.type !== "text") {
        return ResponseManager.processResponse(parsed);
      }

      // 일반 스트리밍 텍스트
      return { text: parsed.text || parsed.content || "", isFinal: false };
    } catch (e) {
      return { text: clean, isFinal: false };
    }
  }

  // 객체 형태의 응답 처리 (이미 완성된 응답)
  if (response && typeof response === "object") {
    // 이미 규격에 맞다면 그대로 반환, 아니면 가공
    if (response.text || response.html) return response;
    return ResponseManager.processResponse(response);
  }

  return response;
};
