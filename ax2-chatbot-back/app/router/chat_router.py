import json
from langchain_core.messages import HumanMessage, SystemMessage

from app.providers import llm_model
from app.services.search_service import search_service
from app.services.survey_service import survey_service

from app.core import logger


class ChatRouter:
    def __init__(self):
        self.llm = llm_model

    async def route(self, user_prompt: str, session_id: str):
        # 액션 처리
        if user_prompt == "__START_SURVEY__":
            return survey_service.start_survey(session_id)

        if user_prompt == "__CANCEL_SURVEY__":
            return search_service.handle("설문 취소", session_id)

        intent = await self._detect_intent(user_prompt)

        if intent == "SEARCH":
            return search_service.handle(user_prompt, session_id)
        elif intent == "SURVEY":
            return survey_service.handle(user_prompt, session_id)

        return search_service.handle(user_prompt, session_id)


    async def _detect_intent(self, user_prompt: str):
        system_prompt = """
        너는 사용자 질문을 분석해서 의도를 분류하는 AI다.

        아래 기준을 반드시 따른다:

        [1] SEARCH (정보 검색)
        - 건강 정보, 운동, 식단, 질병, 증상 등에 대한 '정보'를 물어보는 경우
        - 단순 설명, 방법, 원인 등을 알고 싶은 질문

        예시:
        - "운동 뭐가 좋아?"
        - "허리 통증 원인이 뭐야?"
        - "다이어트 식단 추천해줘"

        [2] SURVEY (건강 설문)
        - 사용자의 건강 상태를 '측정', '진단', '체크'하고 싶어하는 경우
        - 설문, 테스트, 평가, 리포트 등을 요청하는 경우

        예시:
        - "건강 설문 하고 싶어"
        - "내 건강 상태를 체크하고 싶어"
        - "건강 리포트 받아보고 싶어"

        [중요 규칙]
        - 정보 요청이면 반드시 SEARCH
        - 상태 확인/평가 요청이면 반드시 SURVEY
        - 애매하면 SEARCH로 분류

        반드시 아래 JSON 형식으로만 답변:
        {"intent": "SEARCH"} 또는 {"intent": "SURVEY"}

        절대 다른 설명을 추가하지 마라.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = await self.llm.ainvoke(messages)

        logger.info(f"[ROUTER RAW] {response.content}")

        try:
            content = response.content.strip()

            if "{" in content:
                content = content[content.index("{"):]

            result = json.loads(content)
            intent = result.get("intent", "SEARCH")

            intent = intent.strip().upper()

            logger.info(f"[ROUTER] intent={intent} | prompt={user_prompt}")

            return intent
        except Exception:
            logger.error("[ROUTER] JSON 파싱 실패 → fallback SEARCH")
            return "SEARCH"


chat_router = ChatRouter()