import asyncio
from typing import Any

from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage

from app.core import logger
from app.schemas import ChatResponse
from app.utils.file_utils import load_prompt_file
from app.providers import llm_model, public_tools
from app.services.redis_service import redis_service


class SearchService:
    def __init__(self):
        self.llm = llm_model
        self.tools = public_tools
        self.tool_handlers = {tool.name: tool for tool in self.tools}
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.final_response_prompt = load_prompt_file("public-guide.txt")

    async def handle(self, user_prompt: str, session_id: str):

        # 1. RAG 핵심 로직
        rag_result = await self._prepare_search_context(user_prompt, session_id)

        messages = rag_result["llm_input_messages"]

        # 2. streaming
        full_ai_response = ""

        async for chunk, acc in self._stream_llm_response(messages):
            full_ai_response = acc
            yield f"data: {ChatResponse(text=chunk).model_dump_json()}\n\n"

        # 3. 저장
        await self._save_chat(session_id, user_prompt, full_ai_response)

    async def _prepare_search_context(self, user_prompt: str, session_id: str):

        logger.info("[RAG] core 실행")

        # 이전 대화
        past_messages = await redis_service.get_recent_messages(session_id)

        # context 구성
        current_messages = self._build_conversation_context(user_prompt, past_messages)

        # tool 판단
        response = await self._decide_tool_usage(current_messages)

        # tool 실행
        tool_results = await self._execute_tools(response)

        # 최종 메시지 구성
        llm_input_messages = self._compose_llm_messages(
            user_prompt, tool_results, past_messages
        )

        return {
            "llm_input_messages": llm_input_messages,
            "user_prompt": user_prompt,
            "session_id": session_id,
        }

    async def _stream_llm_response(self, messages):

        full_ai_response = ""

        async for chunk in self._generate_llm_stream(messages):
            full_ai_response += chunk
            yield chunk, full_ai_response

    @staticmethod
    async def _save_chat(session_id, user_prompt, ai_response):
        try:
            await redis_service.save_messages(session_id, user_prompt, ai_response)
            logger.info("[SAVE] 대화 저장 완료")
        except Exception as e:
            logger.error(f"[REDIS ERROR] 저장 실패: {str(e)}")

    @staticmethod
    def _build_conversation_context(user_prompt: str, past_messages: list[BaseMessage]) -> list[BaseMessage]:
        human_messages = [msg for msg in past_messages if isinstance(msg, HumanMessage)]
        logger.info(f"[CONTEXT] {len(human_messages)}개의 히스토리")

        if not human_messages:
            return [HumanMessage(content=user_prompt)]

        past_context_text = "\n".join([f"- {msg.content}" for msg in human_messages])

        merged_prompt = (
            f"[이전 대화 맥락]\n"
            f"{past_context_text}\n\n"
            f"[현재 질문]\n"
            f"{user_prompt}"
        )

        return [HumanMessage(content=merged_prompt)]

    async def _decide_tool_usage(self, messages: list[BaseMessage]) -> AIMessage:
        response = await self.llm_with_tools.ainvoke(messages)

        if response.tool_calls:
            logger.info(f"[TOOL] {len(response.tool_calls)}개 호출")
        else:
            logger.info("[TOOL] 미사용")

        return response

    async def _execute_tools(self, response: AIMessage):
        if response.tool_calls:
            tool_messages = await self._execute_tool_calls(response.tool_calls)
            return [response] + list(tool_messages)
        return []

    async def _execute_tool_calls(self, tool_calls) -> tuple[Any]:

        async def run_single_tool(tool_call) -> ToolMessage:
            function_name = tool_call["name"]
            args = tool_call["args"]
            tool_call_id = tool_call["id"]

            handler = self.tool_handlers.get(function_name)

            try:
                tool_result = await handler.ainvoke(args) if handler else "도구 없음"
            except Exception as e:
                logger.error(f"[TOOL ERROR] {e}")
                tool_result = "도구 실행 오류"

            return ToolMessage(
                tool_call_id=tool_call_id,
                name=function_name,
                content=str(tool_result)
            )

        return await asyncio.gather(*(run_single_tool(tc) for tc in tool_calls))

    @staticmethod
    def _compose_llm_messages(user_prompt: str, tool_results: list, past_messages: list[BaseMessage]) -> list[BaseMessage]:
        processed_messages = []

        for msg in past_messages:
            if isinstance(msg, AIMessage):
                clean_content = msg.content.split('[참고 자료]')[0]
                processed_messages.append(AIMessage(content=clean_content.strip()))
            else:
                processed_messages.append(msg)

        return processed_messages + [HumanMessage(content=user_prompt)] + tool_results

    async def _generate_llm_stream(self, messages: list[BaseMessage]):
        system_message = SystemMessage(content=self.final_response_prompt)
        final_messages = [system_message] + messages

        async for chunk in self.llm.astream(final_messages):
            if chunk.content:
                yield chunk.content


search_service = SearchService()