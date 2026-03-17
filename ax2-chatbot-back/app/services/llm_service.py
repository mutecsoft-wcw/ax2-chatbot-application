import json
import logging
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_elasticsearch import ElasticsearchStore
from app.core.config import settings

# log 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LlmService:
    def __init__(self):
        # 임베딩 모델 설정
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.embedding.get("api_key", "EMPTY"),
            base_url=settings.embedding["base_url"],
            model=settings.embedding["text_model"]
        )

        # LLM 모델 설정
        self.llm = ChatOpenAI(
            api_key=settings.llm.get("api_key", "EMPTY"),
            base_url=settings.llm["base_url"],
            model=settings.llm["model_name"],
            temperature=settings.llm.get("temperature", 0.7),
            max_tokens=settings.llm.get("max_token")
        )

        # elasticsearch 설정
        self.vector_store = ElasticsearchStore(
            es_url=settings.elasticsearch["host"],
            index_name=settings.elasticsearch["indices"]["doc_index"],
            embedding=self.embeddings,
            strategy=ElasticsearchStore.ApproxRetrievalStrategy(),
            vector_query_field="text_vector",
            query_field="content"
        )

        # 프롬프트 템플릿 정의
        # 현재 파일(llm_service.py)이 있는 폴더 경로 (app/services)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 상위 폴더(app)로 이동
        base_dir = os.path.dirname(current_dir)

        # app 폴더 아래에 있는 prompt/public-guide.txt 경로를 안전하게 합치기
        prompt_file_path = os.path.join(base_dir, "prompt", "public-guide.txt")
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            system_prompt_text = f.read()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{user_input}")
        ])

        # 출력 Parser (JSON에서 텍스트만 추출)
        self.output_parser = StrOutputParser()

        # 세션별 대화 기록 저장소
        self.store = {}

        self.chain = (
                self.prompt |
                self.llm |
                self.output_parser
        )

    # 특정 세션 ID에 해당하는 대화 내역을 가져오는 함수
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()

        if len(self.store[session_id].messages) > 10:
            self.store[session_id].messages = self.store[session_id].messages[-10:]

        return self.store[session_id]

    async def get_chat_response(self, user_prompt: str, session_id: str):
        # 텍스트를 바로 엘라스틱서치에 검색
        try:
            docs = await self.vector_store.asimilarity_search(user_prompt, k=5)
        except Exception as e:
            logger.error(f"Elasticsearch search failed: {e}")
            error_content = json.dumps({"text": f"검색 중 에러가 발생했어: {str(e)}"}, ensure_ascii=False)
            yield f"data: {error_content}\n\n"
            return

        context_parts = []
        for i, doc in enumerate(docs):
            # 딕셔너리 형태의 메타데이터를 "키: 값, 키: 값" 문자열로 변환
            meta_info = ", ".join([f"{k}: {v}" for k, v in doc.metadata.items()])

            # 본문과 부가정보 합치기
            doc_text = f"--- 문서 {i + 1} ---\n[부가정보] {meta_info}\n[본문 내용]\n{doc.page_content}"
            context_parts.append(doc_text)

        # 최종 프롬프트에 들어갈 context_text 완성
        context_text = "\n\n".join(context_parts)

        with_message_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="user_input",
            history_messages_key="history"
        )

        try:
            async for chunk in with_message_history.astream(
                    {"user_input": user_prompt, "context": context_text},
                    config={"configurable": {"session_id": session_id}}
            ):
                if chunk:
                    content = json.dumps({"text": str(chunk)}, ensure_ascii=False)
                    yield f"data: {content}\n\n"

        except Exception as e:
            logger.error(f"Error during chain execution: {e}")
            error_content = json.dumps({"text": f"Error: {str(e)}"}, ensure_ascii=False)
            yield f"Error: {error_content}\n\n"


llm_service = LlmService()
