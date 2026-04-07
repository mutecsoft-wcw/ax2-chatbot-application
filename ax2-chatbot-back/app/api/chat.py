from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import LlmRequest
from app.services import public_chat_service, internal_chat_service

router = APIRouter()


# 대국민 ChatBot Api
@router.post("/public/stream-chat")
async def chat(request: LlmRequest):
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
async def chat(request: LlmRequest):
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