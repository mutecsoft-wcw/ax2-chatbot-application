import asyncio
import os
from elasticsearch import AsyncElasticsearch

async def check_connection():
    es = AsyncElasticsearch("http://192.168.0.250:19200")
    
    try:
        info = await es.info()
        print("연결 성공!")
        print(f"ES 버전: {info['version']['number']}")
        
        indices = await es.indices.get_alias(index="*")
        print(f"현재 인덱스 목록: {list(indices.keys())}")
        
    except Exception as e:
        print(f"연결 실패: {e}")
    finally:
        await es.close()

if __name__ == "__main__":
    asyncio.run(check_connection())