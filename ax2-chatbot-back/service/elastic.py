import os
from elasticsearch import AsyncElasticsearch
from config.config import settings

es_url = os.getenv("ELASTICSEARCH_URL")
es = AsyncElasticsearch(es_url, headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"})

async def search_es_data(query_text: str, index_name: str = "chs_guide_docs"):

    try:
        response = await es.search(
            index=index_name,
            body={
                "query": {
                    "match": {
                        "content": content  # 검색할 필드명에 맞게 수정
                    }
                }
            }
        )
        # 검색 결과 중 상위 문서들의 텍스트만 추출
        hits = response['hits']['hits']
        return [hit['_source']['content'] for hit in response['hits']['hits']]
    except Exception as e:
        print(f"ES 검색 에러: {e}")
        return []