from .es import es_client


async def search_chs_guide_tool(query: str) -> str:
    """
    엘라스틱서치에서 가이드 문서를 검색해서 텍스트로 반환하는 함수
    """

    docs = await es_client.ainvoke(query)
    print(docs)


    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다. 다른 키워드로 다시 검색해주세요."

    # 검색된 문서들의 본문과 메타데이터를 예쁘게 텍스트로 조립
    formatted_results = []
    for i, doc in enumerate(docs):
        # 만약 ES에 'title' 같은 메타데이터가 있다면 활용
        title = doc.metadata.get("title", "제목 없음")
        content = doc.page_content

        info = f"[문서 {i+1}] {title}\n내용: {content}"
        formatted_results.append(info)

    # LLM이 읽기 좋게 하나의 문자열로 합쳐서 반환
    return "\n\n".join(formatted_results)


# 3. Gemma 3에게 알려줄 도구 명세서 (JSON Schema)
rag_tool_schema = {
    "type": "function",
    "function": {
        "name": "search_chs_guide_tool",
        "description": "지역사회건강조사 이용지침서의 내용을 검색합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색할 구체적인 키워드나 짧은 문장"
                }
            },
            "required": ["query"]
        }
    }
}