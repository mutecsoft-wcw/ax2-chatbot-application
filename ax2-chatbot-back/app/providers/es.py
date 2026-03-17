from elasticsearch import Elasticsearch
from app.core import settings, logger


def get_es_client():
    try:
        client = Elasticsearch(
            settings.elasticsearch["host"],
        )
        return client
    except Exception as e:
        logger.critical(f"Elasticsearch 연결 실패: {e}")
        raise


es_client = get_es_client()
