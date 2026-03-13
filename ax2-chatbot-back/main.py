from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from config.config import setup_cors
from service.chatbot import generate_chatbot_stream

app = FastAPI()

# CORS 설정 적용
setup_cors(app)

class ChatRequest(BaseModel):
    messages: list

@app.post("/stream-chat")
async def chat(request: ChatRequest):
    user_text = request.messages[-1]["text"] if request.messages else ""
    return StreamingResponse(
        generate_chatbot_stream(user_text),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)