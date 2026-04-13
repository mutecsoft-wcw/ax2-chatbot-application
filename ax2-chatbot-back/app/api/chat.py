from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.schemas.chat import LlmRequest
from app.services import public_chat_service, internal_chat_service, redis_service

router = APIRouter()


# 대국민 ChatBot Api
@router.post("/public/stream-chat")
async def public_chat(request: LlmRequest):
    user_input = ""
    session_id = request.sessionId

    if request.messages:
        last_message = request.messages[-1]
        user_input = last_message.get("text") or last_message.get("content") or str(last_message)

    return StreamingResponse(
        public_chat_service.stream_chat(
            user_prompt=user_input,
            session_id=session_id
        ),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
    )

# 업무지원 ChatBot Api
@router.post("/internal/stream-chat")
async def internal_chat(request: LlmRequest):
    user_input = ""
    session_id = request.sessionId

    if request.messages:
        last_message = request.messages[-1]
        user_input = last_message.get("text") or last_message.get("content") or str(last_message)

    return StreamingResponse(
        internal_chat_service.stream_chat(
            user_prompt=user_input,
            session_id=session_id
        ),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
    )

# 대화 내역 조회
@router.get("/history")
async def chat_history(sessionId: str = Query(None, description="조회할 세션 ID")):
    # RequestParam형식으로 요청을 보내야함
    # ex) /history?sessionId=session_id
    return await redis_service.get_chat_history(sessionId)