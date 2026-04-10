import uuid
from typing import List, Dict, Any
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
    def get_recent_messages(self, session_id: str) -> list[BaseMessage]:
        history = self._get_history_obj(session_id)
        all_past_messages = history.messages

        if not all_past_messages:
            return []

        past_messages = all_past_messages[-self.redis_message_limit:]
        logger.info(f"[CONTEXT] 히스토리 총 {len(all_past_messages)}개 중 최신 {len(past_messages)}개 로드")
        return past_messages

    # 대화 기록 저장
    def save_messages(self, session_id: str, user_prompt: str, ai_response: str):
        history = self._get_history_obj(session_id)
        history.add_user_message(user_prompt)
        history.add_ai_message(ai_response)
        logger.info(f"[HISTORY] 대화 기록 저장 완료 (Session: {session_id}, TTL 갱신)")


redis_service = RedisService()