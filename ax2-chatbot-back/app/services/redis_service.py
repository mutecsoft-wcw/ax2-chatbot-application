import json, uuid, asyncio
from typing import Dict, Any
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, messages_from_dict

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
    async def get_chat_history(self, session_id: str | None) -> Dict[str, Any]:
        # 1. 세션 ID가 아예 없는 경우 (완전 처음 방문)
        if not session_id:
            new_id = self.generate_new_session_id()
            logger.info(f"[REDIS] 신규 세션 발급 (최초 방문): {new_id}")
            return {"sessionId": new_id, "history": []}

        history_obj = self._get_history_obj(session_id)
        all_messages = await asyncio.to_thread(lambda: history_obj.messages)

        # 2. 세션 ID는 있는데 Redis에 데이터가 없는 경우 (만료됨)
        if not all_messages:
            return {"sessionId": session_id, "history": []}

        # 4. LangChain 메시지 객체를 프론트엔드(DeepChat) 포맷으로 변환
        formatted_history = [
            {"role": "user" if isinstance(msg, HumanMessage) else "ai", "text": msg.content}
            for msg in all_messages
        ]

        logger.info(f"[REDIS] 히스토리 로드 성공: {session_id} (메시지 {len(formatted_history)}개)")

        return {"sessionId": session_id, "history": formatted_history}

    # 최근 대화 내역 조회 (챗봇 전용)
    async def get_recent_messages(self, session_id: str) -> list[BaseMessage]:
        history = self._get_history_obj(session_id)

        raw_messages = await asyncio.to_thread(
            history.redis_client.lrange,
            history.key,
            0,
            self.redis_message_limit - 1
        )
        
        if not raw_messages:
            return []

        # 가져온 메시지들을 시간순(과거->최신)으로 정렬하기 위해 역순[::-1] 처리
        items = [json.loads(m.decode("utf-8") if isinstance(m, bytes) else m) for m in raw_messages[::-1]]
        past_messages = messages_from_dict(items)
        
        # LLM의 alternating(User/AI 교차) 규칙을 맞추기 위해, 시작이 AIMessage라면 제거
        while past_messages and isinstance(past_messages[0], AIMessage):
            past_messages.pop(0)
            
        logger.info(f"[REDIS] 최근 대화 내역 DB 로드 완료 (Session: {session_id}, {len(past_messages)}개)")
        return past_messages

    # 대화 저장
    async def save_messages(self, session_id: str, user_prompt: str, ai_response: str):
        history = self._get_history_obj(session_id)

        # 여러 개의 동기 작업을 하나의 스레드로 묶어서 실행
        def _sync_save():
            history.add_messages([
                HumanMessage(content=user_prompt),
                AIMessage(content=ai_response)
            ])

        await asyncio.to_thread(_sync_save)
        logger.info(f"[HISTORY] 대화 기록 저장 완료 (Session: {session_id}, TTL 갱신)")


redis_service = RedisService()