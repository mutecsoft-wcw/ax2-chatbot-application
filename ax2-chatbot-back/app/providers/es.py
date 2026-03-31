from langchain_elasticsearch import ElasticsearchStore

from app.core import settings, logger
from .embedding import embedding_model

def get_rag_retriever():
    try:
        es_store = ElasticsearchStore(
            es_url=settings.elasticsearch["host"],
            index_name=settings.elasticsearch["indices"]["chs_raw_guide_index"],
            embedding=embedding_model,
            query_field="content",
            vector_query_field="text_vector"
        )

        retriever = es_store.as_retriever(search_kwargs={"k": 5})

        logger.info("Elasticsearch Retriever 로드 성공!")
        return retriever

    except Exception as e:
        logger.critical(f"RAG 검색 클라이언트 로드 실패: {e}")
        raise

es_client = get_rag_retriever()