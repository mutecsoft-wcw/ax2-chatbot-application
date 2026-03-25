from openai import AsyncOpenAI
from app.core import settings, logger


def get_llm():
    try:
        return AsyncOpenAI(
            api_key=settings.llm["api_key"],
            base_url=settings.llm["base_url"],
        )
    except Exception as e:
        logger.critical(f"LLM 클라이언트 로드 실패: {e}")
        raise

llm_config = {
    "model": settings.llm["model_name"],
    "temperature": settings.llm["temperature"],
    "max_tokens": settings.llm["max_tokens"],
}

llm_model = get_llm()
