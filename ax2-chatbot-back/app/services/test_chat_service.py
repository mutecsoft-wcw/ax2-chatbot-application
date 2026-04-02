from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.output_parsers import StrOutputParser

from app.core import logger
from app.schemas import ChatResponse
from app.utils.file_utils import load_prompt_file
from app.providers import llm_model, tools

class TestChatService:
    def __init__(self):
        self.llm = llm_model
        self.tools = tools

        self.search_prompt = ChatPromptTemplate.from_messages([
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, self.search_prompt)

        # TOOL호출 전용 에이전트
        self.search_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            # return_intermediate_steps=True,
            max_iterations=5,
            max_execution_time=60,
        )

        self.final_guide = load_prompt_file("public-guide.txt")
        self.final_prompt = ChatPromptTemplate.from_messages([
            ("system", self.final_guide),
            ("human", "사용자 질문: {user_input}\n\n[검색된 참고 자료]\n{context}")
        ])

        # 최종답변 생성 체인
        self.final_chain = self.final_prompt | self.llm | StrOutputParser()

    async def get_chat_response(self, user_prompt: str):
        try:
            logger.info(f"[STEP 1] 검색 에이전트 가동: {user_prompt[:50]}...")

            search_result = await self.search_executor.ainvoke({"input": user_prompt})
            context_data = search_result["output"]

            logger.info(f"[STEP 1 완료] 수집된 데이터 확보 성공")

            logger.info(f"[STEP 2] 최종 답변 스트리밍 시작")

            async for chunk in self.final_chain.astream({
                "user_input": user_prompt,
                "context": context_data
            }):
                if chunk:
                    yield f"data: {ChatResponse(text=chunk).model_dump_json()}\n\n"

            logger.info(f"[STEP 2 완료] 스트리밍 정상 종료")

        except Exception as e:
            logger.error(f"[CRITICAL ERROR] {str(e)}", exc_info=True)
            error_response = ChatResponse(text="서비스 처리 중 오류가 발생했습니다.")
            yield f"data: {error_response.model_dump_json()}\n\n"

test_chat_service = TestChatService()