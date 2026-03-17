import json
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_elasticsearch import ElasticsearchStore

from app.core import settings, logger
from app.schemas import ChatResponse
from app.providers import llm_model, embedding_model, es_client


class ChatService:
    def __init__(self):
        # 임베딩 모델 설정
        self.embeddings = embedding_model

        # LLM 모델 설정
        self.llm = llm_model

        # Vector Store 설정
        self.vector_store = ElasticsearchStore(
            es_connection=es_client,
            index_name=settings.elasticsearch["indices"]["doc_index"],
            embedding=self.embeddings,
            strategy=ElasticsearchStore.ApproxRetrievalStrategy(),
            vector_query_field="text_vector",
            query_field="content"
        )

        # 프롬프트 및 체인 초기화
        self._setup_chain()
        self.store = {}

    def _setup_chain(self):
        base_dir = Path(__file__).resolve().parent.parent
        prompt_path = base_dir / "prompt" / "public-guide.txt"

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt_content = f.read()

            self.prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt_content + "\n\n[참고 자료]\n{context}"),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{user_input}")
            ])

            self.output_parser = StrOutputParser()
            self.chain = self.prompt | self.llm | self.output_parser

        except FileNotFoundError:
            logger.critical(f"시스템 프롬프트 파일을 찾을 수 없습니다.: {prompt_path}")
            raise

    async def get_chat_response(self, user_prompt: str, session_id: str):
        # 1. 문서 검색
        try:
            docs = await self.vector_store.asimilarity_search(user_prompt, k=5)
            context_text = self._format_docs(docs)
        except Exception as e:
            logger.error(f"검색 실패: {e}")
            yield f"data: {json.dumps({'text': '자료 검색 중 오류가 발생했습니다.'})}\n\n"
            return

        # 2. 히스토리 관리 설정
        with_message_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="user_input",
            history_messages_key="history"
        )

        # 3. 답변 생성 및 스트리밍
        try:
            async for chunk in with_message_history.astream(
                    {"user_input": user_prompt, "context": context_text},
                    config={"configurable": {"session_id": session_id}}
            ):
                if chunk:
                    response_data = ChatResponse(text=str(chunk))
                    content = response_data.model_dump_json()
                    yield f"data: {content}\n\n"

        except Exception as e:
            logger.error(f"Error during chain execution: {e}")
            yield f"data: {json.dumps({'text': '답변 생성 중 오류가 발생했습니다.'})}\n\n"

    # TODO[sjh] 대화 저장 방식 session_id를 기억하는 방식 임시 구현. 추후 논의 필요.
    # 특정 세션 ID에 해당하는 대화 내역을 가져오는 함수
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()

        # 최근 10개 메시지만 유지
        if len(self.store[session_id].messages) > 10:
            self.store[session_id].messages = self.store[session_id].messages[-10:]

        return self.store[session_id]

    def _format_docs(self, docs):
        context_parts = []
        for i, doc in enumerate(docs):
            # 모든 메타데이터 필드를 문자열로 변환
            meta_info = "\n".join([f"- {k}: {v}" for k, v in doc.metadata.items()])
            doc_text = (
                f"--- 참고 문서 {i + 1} ---\n"
                f"{meta_info}\n"
                f"- 본문: {doc.page_content}"
            )
            context_parts.append(doc_text)

        return "\n\n".join(context_parts)


chat_service = ChatService()
