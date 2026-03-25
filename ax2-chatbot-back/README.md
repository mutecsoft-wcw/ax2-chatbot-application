# AX2 Chatbot Backend Application

## 프로젝트 구조 (Project Structure)

```text
ax2-chatbot-back
├── app 
│   ├── api                            # API 엔드포인트 레이어 (Router)
│   │   └── chat.py                    # 챗봇 관련 요청 핸들러
│   │
│   ├── core                           # 핵심 설정 및 미들웨어
│   │   ├── config.py                  # YAML/환경변수 기반 전역 설정 관리
│   │   └── security.py                # 인증/인가 및 보안 유틸리티
│   │
│   ├── prompt                         # LLM 프롬프트 파일 관리
│   │   ├── public-guide.txt           # 헬스버디 페르소나 및 최종 답변용 프롬프트
│   │   └── tool-router-prompt-kor.txt # 도구 호출(Function Calling) 판단용 프롬프트
│   │
│   ├── providers                      # 외부 인프라 및 서비스 어댑터 (Adapter Layer)
│   │   ├── elasticsearch.py           # Elasticsearch 클라이언트 연결
│   │   ├── embedding.py               # 텍스트 임베딩 모델 연결 및 로드
│   │   └── llm.py                     # LLM(대형 언어 모델) 인스턴스 생성
│   │
│   ├── schemas                        # 데이터 검증 및 직렬화 (Pydantic Models)
│   │   └── chat.py                    # 챗봇 요청/응답 DTO 정의
│   │   └── chat_tools.py              # Tool 정의
│   │
│   ├── services                       # 비즈니스 로직 (Service Layer)
│   │   ├── chat_service.py            # LLM 대화 흐름 제어, Function Calling 및 스트리밍 처리
│   │   └── search_service.py          # Elasticsearch 기반 RAG 문서 검색 로직
│   │
│   ├── utils                          # 비즈니스 로직 (Service Layer)
│   │   └── file_utils.py              # 파일 관련 유틸리티
│   │
│   └── main.py                        # FastAPI 애플리케이션 진입점 및 초기화
│   
├── config.yml                         # 시스템 설정값 관리 (모델명, 엔드포인트 등)
└── requirements.txt                   # Python 의존성 패키지 목록
```