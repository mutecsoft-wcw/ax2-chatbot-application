
```text
project_root/
├── app/
│   ├── main.py               # FastAPI 진입점
│   ├── core/                 # 프로젝트 공통 핵심 설정
│   │   ├── config.py         # YAML 설정 파일 로드 및 환경변수 관리
│   │   └── security.py       # 보안 관련 유틸리티
│   ├── api/                  # API 엔드포인트 레이어
│   │   └── chat.py           # 챗봇 관련 요청 핸들러 (Router)
│   ├── services/             # 비즈니스 로직 레이어 (Core Logic)
│   │   ├── llm_service.py    # LangChain 기반 RAG/Chat 흐름 제어
│   │   └── search_service.py # 엘라스틱서치 검색 로직 및 쿼리 최적화
│   ├── providers/            # 외부 서비스 및 인프라 연결 인터페이스
│   │   ├── llm.py            # LLM 모델 인스턴스 생성
│   │   ├── embedding.py      # 텍스트 임베딩 모델 로드
│   │   └── elasticsearch.py  # Elasticsearch 클라이언트 연결 설정
│   └── schemas/              # 데이터 검증 레이어
│       └── chat.py           # 요청/응답을 위한 Pydantic 모델 정의
├── config.yml                # 시스템 설정값 관리 (모델명, 엔드포인트 등)
├── requirements.txt          # 의존성 패키지 목록
```