import os
import json
from openai import AsyncOpenAI
from config.config import settings
from service.elastic import search_es_data

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

async def generate_chatbot_stream(user_text: str):
    try:
        # ES에서 관련 지식 검색
        context_docs = await search_es_data(user_text)
        context = "\n".join(context_docs) if context_docs else "관련 건강 정보가 지식 베이스에 없습니다."

        # 프롬프트 구성 (RAG)
        base_prompt = load_prompt()
        final_prompt = base_prompt.format(context=context, user_text=user_text)
        
        # LLM 호출
        stream = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": user_text}],
            stream=True
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'text': content}, ensure_ascii=False)}\n\n"

        # 이미지 처리 로직 등도 여기에 포함
        if "이미지" in user_text:
            payload = {"type": "images", "text": "\n이미지 결과입니다.", "data": ["https://picsum.photos/400/300"]}
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"