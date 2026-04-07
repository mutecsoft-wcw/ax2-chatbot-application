import asyncio
from typing import Any

from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.core import logger, settings
from app.schemas import ChatResponse
from app.utils.file_utils import load_prompt_file
from app.providers import llm_model, tools


class PublicChatService:
    def __init__(self):
        self.llm = llm_model
        self.tools = tools
        self.tool_handlers = {tool.name: tool for tool in self.tools}
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.final_response_prompt = load_prompt_file("public-guide.txt")
        self.redis_url = settings.redis["url"]
        self.redis_ttl = settings.redis["ttl"]
        self.redis_message_limit = settings.redis["message_limit"]

    async def stream_chat(self, user_prompt: str, session_id: str):
        try:
            # 1. 이전 대화내역 로드 및 메시지 초기화
            logger.info(f"[STEP 1] 대화 요청 수신: {user_prompt[:50]}...")
            current_messages = self._load_context_messages(session_id, user_prompt)

            # 2. 도구 호출 여부 판단 및 실행
            logger.info(f"[STEP 2] LLM 도구 호출 여부 판단")
            response = await self._router_tool(current_messages)

            # 3. 도구 결과 처리 및 자료 검색
            logger.info(f"[STEP 3] 도구 호출 결과 처리 및 파이프라인 실행")
            messages_for_final = await self._process_tool_results(response, current_messages)

            # 4. 최종 답변 생성 및 스트리밍
            logger.info(f"[STEP 4] 최종 답변 스트리밍 시작")
            full_ai_response = ""
            async for text_chunk in self._stream_final_response(messages_for_final):
                full_ai_response += text_chunk

                yield f"data: {ChatResponse(text=text_chunk).model_dump_json()}\n\n"

            # 5. 최종 대화 내역 저장
            self._save_context_history(session_id, user_prompt, full_ai_response)
            logger.info(f"[STEP 5] 대화 기록 저장 완료 및 스트리밍 종료")

        except Exception as e:
            logger.error(f"[CRITICAL ERROR] {str(e)}", exc_info=True)
            error_response = ChatResponse(text="서비스 처리 중 오류가 발생했습니다.")
            yield f"data: {error_response.model_dump_json()}\n\n"

    # --- [STEP 1] ---
    def _load_context_messages(self, session_id: str, user_prompt: str) -> list[BaseMessage]:
        history = self._get_message_history(session_id)
        all_past_messages = history.messages

        if not all_past_messages:
            return [HumanMessage(content=user_prompt)]

        past_messages = all_past_messages[-self.redis_message_limit:] if all_past_messages else []
        logger.info(f"[CONTEXT] 히스토리 총 {len(all_past_messages)}개 중 최신 {len(past_messages)}개 로드")
        return past_messages + [HumanMessage(content=user_prompt)]

    # --- [STEP 2] ---
    async def _router_tool(self, messages: list[BaseMessage]) -> AIMessage:
        response = await self.llm_with_tools.ainvoke(messages)
        logger.info(f"[STEP 2] 도구 판별 LLM 답변: {response}")

        if response.tool_calls:
            logger.info(f"[STEP 2] 도구 호출 감지: {len(response.tool_calls)}개")
        else:
            logger.info(f"[STEP 2] 도구 미사용 (일반 대화)")

        return response

    # --- [STEP 3] ---
    async def _process_tool_results(self, response: AIMessage, messages: list[BaseMessage]):
        if response.tool_calls:
            logger.info(f"[STEP 3] 도구 실행 파이프라인 진입")
            current_messages = messages + [response]
            tool_messages = await self._execute_tool_calls(response.tool_calls)
            return current_messages + list(tool_messages)
        else:
            logger.info(f"[STEP 3] 도구 미사용 판단. 일반 대화 처리")
            return messages

    async def _execute_tool_calls(self, tool_calls) -> tuple[Any]:
        async def run_single_tool(tool_call) -> ToolMessage:
            function_name = tool_call["name"]
            args = tool_call["args"]
            tool_call_id = tool_call["id"]

            handler = self.tool_handlers.get(function_name)
            if handler:
                try:
                    tool_result = await handler.ainvoke(args)
                    logger.info(f"[STEP 3-RESULT] {function_name} 도구 실행 완료 (결과 길이: {len(str(tool_result))}자)")
                except Exception as e:
                    logger.error(f"[TOOL ERROR] 도구 '{function_name}' 실행 중 오류 발생: {e}", exc_info=True)
                    tool_result = f"도구 '{function_name}'을(를) 실행하는 중 오류가 발생했습니다."
            else:
                logger.warning(f"[WARNING] 알 수 없는 도구 호출: {function_name}")
                tool_result = "해당 기능을 수행할 수 있는 도구를 찾을 수 없습니다."

            return ToolMessage(
                tool_call_id=tool_call_id,
                name=function_name,
                content=str(tool_result)
            )

        return await asyncio.gather(*(run_single_tool(tc) for tc in tool_calls))

    # --- [STEP 4] ---
    async def _stream_final_response(self, messages: list[BaseMessage]):
        system_message = SystemMessage(content=self.final_response_prompt)
        final_messages = [system_message] + messages

        async for chunk in self.llm.astream(final_messages):
            if chunk.content:
                yield chunk.content

    # --- [STEP 5] ---
    def _save_context_history(self, session_id: str, user_prompt: str, ai_response: str):
        history = self._get_message_history(session_id)
        history.add_user_message(user_prompt)
        history.add_ai_message(ai_response)
        logger.info(f"[HISTORY] 대화 기록 저장 완료 (Session: {session_id}, TTL 갱신)")

    def _get_message_history(self, session_id: str) -> RedisChatMessageHistory:
        return RedisChatMessageHistory(session_id, url=self.redis_url, ttl=self.redis_ttl)


public_chat_service = PublicChatService()