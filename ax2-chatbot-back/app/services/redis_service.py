from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage

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

    # 최근 대화 내역 조회
    def get_recent_messages(self, session_id: str) -> list[BaseMessage]:
        history = self._get_history_obj(session_id)
        all_past_messages = history.messages

        if not all_past_messages:
            return []

        past_messages = all_past_messages[-self.redis_message_limit:] if all_past_messages else []
        logger.info(f"[CONTEXT] 히스토리 총 {len(all_past_messages)}개 중 최신 {len(past_messages)}개 로드")
        return past_messages

    # 대화 기록 저장
    def save_messages(self, session_id: str, user_prompt: str, ai_response: str):
        history = self._get_history_obj(session_id)
        history.add_user_message(user_prompt)
        history.add_ai_message(ai_response)
        logger.info(f"[HISTORY] 대화 기록 저장 완료 (Session: {session_id}, TTL 갱신)")


redis_service = RedisService()