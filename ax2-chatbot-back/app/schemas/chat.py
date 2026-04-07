from pydantic import BaseModel, Field
from typing import List, Dict, Any


class LlmRequest(BaseModel):
    messages: List[Dict[str, Any]]
    sessionId: str = "default_session"

class ChatResponse(BaseModel):
    text: str = Field(...)