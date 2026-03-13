from pydantic import BaseModel
from typing import List, Dict, Any, Union

class LlmRequest(BaseModel):
    messages: List[Dict[str, Any]]
    session_id: str = "default_session"