from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import LlmRequest
from app.services import chat_service

router = APIRouter()


@router.post("/stream-chat")
async def chat(request: LlmRequest):
    user_input = ""

    if request.messages:
        last_message = request.messages[-1]
        user_input = last_message.get("text") or last_message.get("content") or str(last_message)

    return StreamingResponse(
        chat_service.get_chat_response(user_input),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
    )