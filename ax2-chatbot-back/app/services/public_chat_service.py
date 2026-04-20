from app.core import logger
from app.schemas import ChatResponse
from app.router import chat_router

class PublicChatService:
    def __init__(self):
        self.router = chat_router

    async def stream_chat(self, user_prompt: str, session_id: str):
        try:
            logger.info(f"[STEP 1] 대화 요청 수신: {user_prompt[:50]}...")

            generator = await self.router.route(user_prompt, session_id)

            async for chunk in generator:
                yield chunk

        except Exception as e:
            logger.error(f"[CRITICAL ERROR] {str(e)}", exc_info=True)
            error_response = ChatResponse(text="서비스 처리 중 오류가 발생했습니다.")
            yield f"data: {error_response.model_dump_json()}\n\n"

public_chat_service = PublicChatService()