from langchain_openai import ChatOpenAI

from app.core import settings, logger


def get_llm():
    try:
        return ChatOpenAI(
            api_key=settings.llm["api_key"],
            base_url=settings.llm["base_url"],
            model=settings.llm["model_name"],
            max_tokens=settings.llm["max_tokens"],
            temperature=settings.llm["temperature"],
            streaming=True,
            verbose=True,
            max_retries=3
        )
    except Exception as e:
        logger.critical(f"LLM 클라이언트 로드 실패: {e}")
        raise

llm_model = get_llm()
