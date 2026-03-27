from langchain_openai import OpenAIEmbeddings
from app.core import settings, logger


def get_embeddings():
    try:
        return OpenAIEmbeddings(
            api_key=settings.embedding.get("api_key", "EMPTY"),
            base_url=settings.embedding["base_url"],
            model=settings.embedding["text_model"],
            check_embedding_ctx_length=False,
        )
    except Exception as e:
        logger.critical(f"임베딩 모델 로드 실패: {e}")
        raise


embedding_model = get_embeddings()
