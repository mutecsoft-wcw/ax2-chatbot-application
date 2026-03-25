"""
LLM에 제공될 Function Calling (Tools) 명세를 관리하는 모듈.
"""
from typing import Dict, Any, List, Optional

def create_function_tool(
    name: str,
    description: str,
    properties: Dict[str, Any],
    required: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    LLM Function Calling 표준 형식의 Tool 딕셔너리를 생성하는 헬퍼 함수
    """
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

# --- Tool 인스턴스 정의 ---

search_guide_docs_tool = create_function_tool(
    name="search_guide_docs",
    description="지역사회건강조사 이용지침서의 내용을 검색합니다.",
    properties={
        "query": {
            "type": "string",
            "description": "검색할 핵심 키워드나 문장"
        }
    },
    required=["query"]
)

GUIDE_DOCS_TOOLS = [search_guide_docs_tool]