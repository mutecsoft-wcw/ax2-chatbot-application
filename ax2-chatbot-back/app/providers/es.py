from typing import Any, Optional, Mapping, Union, List
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from langchain_core.documents import Document
from app.core import settings, logger
from .embedding import embedding_model

es_client = AsyncElasticsearch(settings.elasticsearch["host"])

# 지침서 전용 검색 함수 (CHS, KNHANES)
async def search_guide_documents(
        index_name: str,
        query: str,
        year: Optional[Union[int, List[int]]] = None,
        k: int = 5,
        num_candidates: int = 50
) -> str:
    query_vector = embedding_model.embed_query(query)

    knn_body = {
        "field": "text_vector",
        "query_vector": query_vector,
        "k": k,
        "num_candidates": num_candidates,
    }

    if year is None:
        current_year = datetime.now().year
        year = [current_year - i for i in range(4)]
        logger.info(f"연도 미지정 최신 4개년 자동 필터 적용 ({index_name}): {year}")

    if isinstance(year, list):
        knn_body["filter"] = {"terms": {"year": year}}
    else:
        knn_body["filter"] = {"term": {"year": year}}

    body = {
        "knn": knn_body,
        "_source": {"excludes": ["text_vector"]}
    }

    return await _execute_es_search(index_name, body, k)

# 일반 의학정보 전용 검색 함수 (NHIP)
async def search_health_info(
        index_name: str,
        query: str,
        k: int = 5,
        num_candidates: int = 50
) -> str:
    query_vector = embedding_model.embed_query(query)

    knn_body = {
        "field": "text_vector",
        "query_vector": query_vector,
        "k": k,
        "num_candidates": num_candidates,
    }

    body = {
        "knn": knn_body,
        "_source": {"excludes": ["text_vector"]}
    }

    return await _execute_es_search(index_name, body, k)


# Elasticsearch 검색 요청 함수
async def _execute_es_search(index_name: str, body: dict, k: int) -> str:
    try:
        response = await es_client.search(index=index_name, body=body, size=k)
        hits = response.get("hits", {}).get("hits", [])

        docs = [_field_mapper(hit) for hit in hits]
        return _result_formatted(docs)
    except Exception as e:
        logger.critical(f"ES 검색 실패 ({index_name}): {e}")
        return "검색 중 오류가 발생했습니다."

# 메타데이터 생성 로직
def _field_mapper(hit: Mapping[str, Any]) -> Document:
    source = hit.get("_source", {})

    # 벡터 데이터나 본문은 메타데이터에서 제외
    exclude_fields = {"content", "text_vector"}
    metadata = {k: v for k, v in source.items() if k not in exclude_fields}
    metadata["score"] = hit.get("_score")

    return Document(
        page_content=source.get("content", ""),
        metadata=metadata
    )


# 검색 결과 포맷팅 결과
def _result_formatted(docs) -> str:
    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다. 다른 키워드로 다시 검색해주세요."

    formatted_results = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "제목 없음")
        content = doc.page_content
        info = f"[문서 {i + 1}] {source}\n내용: {content}"

        # TODO(sjh) 검색 문서 로깅. 테스트 이후 실제서비스에서는 삭제.
        logger.info(info)
        formatted_results.append(info)

    return "\n\n".join(formatted_results)
