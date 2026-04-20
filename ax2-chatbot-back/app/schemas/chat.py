from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class LlmRequest(BaseModel):
    messages: List[Dict[str, Any]]
    sessionId: str = ""

class ChatResponse(BaseModel):
    text: Optional[str] = None
    type: Optional[str] = "text"
    data: Optional[Dict[str, Any]] = None
    role: Optional[str] = "ai"