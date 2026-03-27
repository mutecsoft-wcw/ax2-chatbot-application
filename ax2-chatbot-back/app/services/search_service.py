from app.core import logger
from app.providers import embedding_model, es_client


class SearchService:
    def __init__(self, index_name: str = "chs-raw-guide-vector"):
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.es_client = es_client

    async def search_guide_docs(self, query: str, top_k: int = 4) -> str:
        """문서 검색 도구 핸들러"""
        logger.info(f"RAG 검색 실행: {query}")

        try:
            query_vector = self.embedding_model.embed_query(query)

            response = await self.es_client.search(
                index=self.index_name,
                body={
                    "size": top_k,
                    "query": {
                        "knn": {
                            "field": "text_vector",
                            "query_vector": query_vector,
                            "k": top_k,
                            "num_candidates": 100
                        }
                    },
                    "_source": ["content", "year", "title", "source", "page_label"]
                }
            )

            hits = response.get("hits", {}).get("hits", [])
            logger.info(f"검색 완료: {len(hits)}건의 문서 발견")

            return self._format_docs(hits)

        except Exception as e:
            logger.error(f"Elasticsearch 검색 중 오류 발생: {e}")
            return "검색 중 오류가 발생했습니다."

    @staticmethod
    def _format_docs(hits: list) -> str:
        if not hits:
            return "검색 결과가 없습니다."

        formatted_results = []
        for i, hit in enumerate(hits):
            source = hit.get("_source", {})
            title = source.get("title", "")
            year = source.get("year", "")
            page = source.get("page_label", "")
            content = source.get("content", "").strip()
            doc_source = source.get("source", "")

            doc_block = (
                f"--- [참고 자료 {i+1}] ---\n"
                f"**문서명**: {title}\n"
                f"**발행연도**: {year}년\n"
                f"**출처**: {doc_source}\n"
                f"**페이지**: {page}\n"
                f"**내용**: {content}"
            )
            formatted_results.append(doc_block)

        return "\n\n".join(formatted_results)


search_service = SearchService()