import uuid, re
from typing import Dict, Any
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.core import logger, settings


class RedisService:
    def __init__(self):
        self.redis_url = settings.redis["url"]
        self.redis_ttl = settings.redis["ttl"]
        self.redis_message_limit = settings.redis["message_limit"]

    # RedisChatMessageHistory 객체 생성
    def _get_history_obj(self, session_id: str) -> RedisChatMessageHistory:
        return RedisChatMessageHistory(
            session_id,
            url=self.redis_url,
            ttl=self.redis_ttl
        )

    # session id 생성
    @staticmethod
    def generate_new_session_id() -> str:
        return f"sess-{uuid.uuid4().hex[:8]}"

    # 최근 대화 내역 조회 (웹 전용)
    def get_chat_history(self, session_id: str | None) -> Dict[str, Any]:
        # 1. 세션 ID가 아예 없는 경우 (완전 처음 방문)
        if not session_id:
            new_id = self.generate_new_session_id()
            logger.info(f"[REDIS] 신규 세션 발급 (최초 방문): {new_id}")
            return {"sessionId": new_id, "history": []}

        history_obj = self._get_history_obj(session_id)
        all_messages = history_obj.messages

        # 2. 세션 ID는 있는데 Redis에 데이터가 없는 경우 (만료됨)
        if not all_messages:
            # new_id = self.generate_new_session_id()
            # logger.info(f"[REDIS] 세션 만료로 인한 신규 발급: {session_id} -> {new_id}")
            return {"sessionId": session_id, "history": []}

        # 4. LangChain 메시지 객체를 프론트엔드(DeepChat) 포맷으로 변환
        formatted_history = []
        for msg in all_messages:
            role = "user" if isinstance(msg, HumanMessage) else "ai"
            formatted_history.append({
                "role": role,
                "text": msg.content
            })

        logger.info(f"[REDIS] 히스토리 로드 성공: {session_id} (메시지 {len(formatted_history)}개)")

        return {
            "sessionId": session_id,
            "history": formatted_history
        }

    # 최근 대화 내역 조회 (챗봇 전용)
    def get_recent_messages(self, session_id: str, only_human: bool = False, clean_ai_format: bool = True) -> list[BaseMessage]:
        history = self._get_history_obj(session_id)
        all_past_messages = history.messages

        if not all_past_messages:
            return []

        # 1. 설정한 limit만큼 최신 메시지 슬라이싱
        past_messages = all_past_messages[-self.redis_message_limit:]

        # 2. [옵션 A] 도구 판별 LLM을 위한 필터링 (사용자 질문만 추출)
        if only_human:
            filtered_messages = [msg for msg in past_messages if isinstance(msg, HumanMessage)]
            logger.info(f"[CONTEXT] 도구 판별용 히스토리 로드: {len(filtered_messages)}개의 HumanMessage만 추출")
            return filtered_messages

        # 3. [옵션 B] 최종 답변 LLM을 위한 AI 응답 정제 (마크다운 포맷 껍데기 벗기기)
        processed_messages = []
        for msg in past_messages:
            if isinstance(msg, AIMessage) and clean_ai_format:
                # [참고 자료] 섹션 통째로 날리기 (LLM이 참고자료를 지어내는 할루시네이션 방지)
                clean_content = msg.content.split('[참고 자료]')[0]

                # 마크다운 헤딩(##, ###) 등 흉내내기 좋은 기호 지우기
                clean_content = re.sub(r'#{1,3}\s', '', clean_content)

                # 새로운 형태의 AIMessage 객체로 복사하여 추가 (원본 Redis 데이터는 훼손 안 됨)
                processed_messages.append(AIMessage(content=clean_content.strip()))
            else:
                processed_messages.append(msg)

        logger.info(f"[CONTEXT] 최종 답변용 히스토리 로드: 총 {len(all_past_messages)}개 중 최신 {len(processed_messages)}개 로드 (포맷 정제 완료)")
        return processed_messages

    # 대화 기록 저장
    def save_messages(self, session_id: str, user_prompt: str, ai_response: str):
        history = self._get_history_obj(session_id)
        history.add_user_message(user_prompt)
        history.add_ai_message(ai_response)
        logger.info(f"[HISTORY] 대화 기록 저장 완료 (Session: {session_id}, TTL 갱신)")


redis_service = RedisService()