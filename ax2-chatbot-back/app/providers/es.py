from typing import Any, Optional, Mapping, Callable

from langchain_elasticsearch import ElasticsearchRetriever
from langchain_core.documents import Document
from app.core import settings, logger
from .embedding import embedding_model


def field_mapper(hit: Mapping[str, Any]) -> Optional[Document]:
    source = hit.get("_source", {})

    exclude_fields = {"content", "text_vector"}
    metadata = {k: v for k, v in source.items() if k not in exclude_fields}
    metadata["score"] = hit.get("_score")

    return Document(
        page_content=source.get("content", ""),
        metadata=metadata
    )

def query_vector_body(vector_field: str, k: int, num_candidates: int) -> Callable[[str], dict[str, Any]]:
    def body_func(query: str) -> dict[str, Any]:
        query_vector = embedding_model.embed_query(query)
        
        return {
            "knn": {
                "query_vector": query_vector,
                "field": vector_field,           # 벡터가 저장된 필드명
                "k": k,                          # 가져올 문서 개수
                "num_candidates": num_candidates # 정확도를 위해 훑어볼 후보군
            }
        }

    return body_func

def get_elasticsearch_retriever(
    index_name: str,
    vector_field: str = "text_vector",
    k: int = 5,
    num_candidates: int = 50,
):
    try:
        retriever = ElasticsearchRetriever.from_es_params(
            index_name=index_name,
            body_func=query_vector_body(vector_field=vector_field, k=k, num_candidates=num_candidates),
            document_mapper=field_mapper,
            url=settings.elasticsearch["host"],
        )

        return retriever

    except Exception as e:
        logger.critical(f"Retriever 로드 실패: {e}")
        raise


chs_raw_guide_retriever = get_elasticsearch_retriever(
    index_name=settings.elasticsearch["indices"]["chs_raw_guide_index"],
    vector_field="text_vector",
    k=3,
    num_candidates=50
)

chs_question_guide_retriever = get_elasticsearch_retriever(
    index_name=settings.elasticsearch["indices"]["chs_question_guide_index"],
    vector_field="text_vector",
    k=3,
    num_candidates=50
)

knhanes_raw_guide_retriever = get_elasticsearch_retriever(
    index_name=settings.elasticsearch["indices"]["knhanes_raw_guide_index"],
    vector_field="text_vector",
    k=3,
    num_candidates=50
)

nhip_health_info_retriever = get_elasticsearch_retriever(
    index_name=settings.elasticsearch["indices"]["nhip_health_info_index"],
    vector_field="text_vector",
    k=3,
    num_candidates=50
)
