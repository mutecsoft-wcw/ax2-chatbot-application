from typing import Any, Optional, Mapping, Union, List
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from langchain_core.documents import Document
from app.core import settings, logger
from .embedding import embedding_model

es_client = AsyncElasticsearch(settings.elasticsearch["host"])

# ==========================================
# 1. 도메인별 검색 함수
# ==========================================
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
        year = [current_year - i for i in range(3)]
        logger.info(f"연도 미지정 최신 3개년 자동 필터 적용 ({index_name}): {year}")

    if isinstance(year, list):
        knn_body["filter"] = {"terms": {"year": year}}
    else:
        knn_body["filter"] = {"term": {"year": year}}

    body = {
        "knn": knn_body,
        "_source": {"excludes": ["text_vector"]}
    }

    docs = await _execute_es_search(index_name, body, k)

    return _result_formatted(docs)

# 질병관리청 국가건강정보 전용 검색 함수
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

    docs = await _execute_es_search(index_name, body, k)

    if isinstance(docs, str):
        return docs

    return _result_formatted(docs)


# 지역사회건강조사 지표 데이터 전용 검색 함수
async def search_indicator_data(
        index_name: str,
        query: str,
        k: int = 5,
        num_candidates: int = 50
) -> Union[List[Document], str]:
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

    docs = await _execute_es_search(index_name, body, k, content_field=None)

    if isinstance(docs, str):
        return docs

    return docs

# ==========================================
# 2. 공통 검색 및 매퍼 로직
# ==========================================
# Elasticsearch 검색 요청 함수
async def _execute_es_search(
        index_name: str,
        body: dict,
        k: int,
        content_field: Optional[str] = "content"
) -> list[Document] | str:
    try:
        response = await es_client.search(index=index_name, body=body, size=k)
        hits = response.get("hits", {}).get("hits", [])

        docs = [_field_mapper(hit, content_field) for hit in hits]
        return docs
    except Exception as e:
        logger.critical(f"ES 검색 실패 ({index_name}): {e}")
        return "검색 중 오류가 발생했습니다."

# 메타데이터 생성 로직
def _field_mapper(hit: Mapping[str, Any], content_field: Optional[str]) -> Document:
    source = hit.get("_source", {})

    # 벡터 데이터나 본문은 메타데이터에서 제외
    exclude_fields = {"text_vector"}
    page_content = ""

    if content_field and content_field in source:
        exclude_fields.add(content_field)
        page_content = str(source.get(content_field, ""))

    metadata = {k: v for k, v in source.items() if k not in exclude_fields}
    metadata["score"] = hit.get("_score")

    return Document(
        page_content=page_content,
        metadata=metadata
    )

# ==========================================
# 3. 포맷터 로직
# ==========================================
# 검색 결과 포맷팅 결과
def _result_formatted(docs) -> str:
    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다. 다른 키워드로 다시 검색해주세요."

    formatted_results = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "제목 없음")
        content = doc.page_content
        score = doc.metadata.get("score", 0.0)

        info = f"[문서 {i + 1}] {source}\n내용: {content}"

        # TODO(sjh) 검색 문서 로깅. 테스트 이후 실제서비스에서는 삭제.
        logger.info(info)
        formatted_results.append(info)

    return "\n\n".join(formatted_results)


# 지표 전용 결과 포맷팅
def _indicator_result_formatted(docs: List[Document]) -> str:
    if not docs:
        return "관련 통계 지표를 찾지 못했습니다. 다른 지표명으로 검색해주세요."

    formatted_results = []
    for i, doc in enumerate(docs):
        metadata = doc.metadata

        score = metadata.get("score", 0.0)
        indicator_name = metadata.get("indicator_name", "지표명 없음")
        category = metadata.get("category", "분류 없음")
        year = metadata.get("year", "연도 미상")
        dimension = metadata.get("dimension", "알 수 없음")
        domain_value = metadata.get("domain_value", "알 수 없음")
        raw_value = metadata.get("value", 0)
        sample_size = metadata.get("sample_size", 0)

        # 1. 값(Value) 포맷팅: 소수점 비율을 퍼센트%로 변환
        if isinstance(raw_value, float) and raw_value <= 1.0:
            display_value = f"{raw_value * 100:.1f}%"
        else:
            display_value = str(raw_value)

        # 2. 도메인 및 디멘전 한글화: LLM이 'All'을 엉뚱하게 해석하지 않도록 처리
        domain_str = "전국" if domain_value == "All" else domain_value
        dimension_str = "전체" if dimension == "total" else dimension

        # 3. LLM이 읽기 쉬운 구조화된 문자열 생성
        info = (
            f"--- [지역사회건강조사 공식 통계 결과 {i + 1}] ---\n"
            f"* 데이터 성격: 실측 통계 수치 (※ 주의: 지침서나 매뉴얼 내용이 아님)\n"
            f"* 연도 및 카테고리: {year}년 / {category}\n"
            f"* 공식 지표명: {indicator_name}\n"
            f"* 조사 지역/특성: {domain_str} ({dimension_str})\n"
            f"* 최종 산출 수치: {display_value} (표본 수: {sample_size}명)\n"
            f"* 출처 명칭: {year}년 지역사회건강조사 통계 결과자료"
        )
        formatted_results.append(info)

    result_text = "지역사회건강조사(CHS) 지표 검색 결과입니다:\n\n" + "\n\n".join(formatted_results)

    # TODO(sjh) 검색 문서 로깅. 테스트 이후 실제서비스에서는 삭제.
    logger.info(f"[지표 검색 결과]\n{result_text}")

    return result_text
