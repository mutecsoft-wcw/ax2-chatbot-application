from langchain_openai import ChatOpenAI
from app.core import settings, logger


def get_llm():
    try:
        return ChatOpenAI(
            api_key=settings.llm.get("api_key", "EMPTY"),
            base_url=settings.llm["base_url"],
            model=settings.llm["model_name"],
            temperature=settings.llm.get("temperature", 0.7),
            max_tokens=settings.llm.get("max_token"),
            streaming=True
        )
    except Exception as e:
        logger.critical(f"LLM 로드 실패: {e}")
        raise


llm_model = get_llm()
