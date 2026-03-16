import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.core.config import settings

class LlmService:
    def __init__(self):
        # LLM 모델 설정
        self.llm = ChatOpenAI(
            api_key=settings.llm.get("api_key", "EMPTY"),
            base_url=settings.llm["base_url"],
            model=settings.llm["model_name"],
            temperature=settings.llm.get("temperature", 0.7),
            max_tokens=settings.llm.get("max_tokens", 2048)
        )

        # 프롬프트 템플릿 정의
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 친절하고 전문적인 AI개발자 친구야."),
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

    # 3. 특정 세션 ID에 해당하는 대화 내역을 가져오는 함수
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()

        if len(self.store[session_id].messages) > 10:
            self.store[session_id].messages = self.store[session_id].messages[-10:]

        return self.store[session_id]

    async def get_chat_response(self, user_prompt: str, session_id:str):
        with_message_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="user_input",
            history_messages_key="history"
        )

        try:
            async for chunk in with_message_history.astream(
                    {"user_input": user_prompt},
                    config={"configurable": {"session_id": session_id}}
            ):
                if chunk:
                    # 1. ensure_ascii=False: 한글을 그대로 출력
                    # 2. + "\n": 각 조각을 줄바꿈으로 구분 (Deep Chat 인식용)
                    content = json.dumps({"text": str(chunk)}, ensure_ascii=False)
                    yield f"data: {content}\n\n"      
                
        except Exception as e:
            yield f"Error: {str(e)}"

llm_service = LlmService()