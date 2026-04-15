import asyncio
from typing import Any

from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage

from app.core import logger
from app.schemas import ChatResponse
from app.utils.file_utils import load_prompt_file
from app.providers import llm_model, internal_tools
from app.services.redis_service import redis_service


class InternalChatService:
    def __init__(self):
        self.llm = llm_model
        self.tools = internal_tools
        self.tool_handlers = {tool.name: tool for tool in self.tools}
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.final_response_prompt = load_prompt_file("internal-guide.txt")

    async def stream_chat(self, user_prompt: str, session_id: str):
        try:
            logger.info(f"[STEP 1] 대화 요청 수신: {user_prompt[:50]}...")

            # 0. 이전 대화내역 로드
            past_messages = await redis_service.get_recent_messages(session_id)

            # 1. 도구 판별용 메시지 초기화
            current_messages = self._load_context_messages(user_prompt, past_messages)

            # 2. 도구 호출 여부 판단 및 실행
            logger.info(f"[STEP 2] LLM 도구 호출 여부 판단")
            response = await self._router_tool(current_messages)

            # 3. 도구 결과 처리 및 자료 검색
            logger.info(f"[STEP 3] 도구 호출 결과 처리 및 파이프라인 실행")
            tool_results = await self._process_tool_results(response)

            # 4. 최종 답변 생성 및 스트리밍
            logger.info(f"[STEP 4] 최종 답변 스트리밍 시작")
            messages_for_final = self._build_final_messages(user_prompt, tool_results, past_messages)

            full_ai_response = ""
            async for text_chunk in self._stream_final_response(messages_for_final):
                full_ai_response += text_chunk
                yield f"data: {ChatResponse(text=text_chunk).model_dump_json()}\n\n"

            # 5. 최종 대화 내역 저장
            try:
                await redis_service.save_messages(session_id, user_prompt, full_ai_response)
                logger.info(f"[STEP 5] 대화 기록 저장 완료 및 스트리밍 종료")
            except Exception as redis_error:
                logger.error(f"[REDIS ERROR] 대화 기록 저장 실패: {str(redis_error)}")

        except Exception as e:
            logger.error(f"[CRITICAL ERROR] {str(e)}", exc_info=True)
            error_response = ChatResponse(text="서비스 처리 중 오류가 발생했습니다.")
            yield f"data: {error_response.model_dump_json()}\n\n"

    # --- [STEP 1] ---
    @staticmethod
    def _load_context_messages(user_prompt: str, past_messages: list[BaseMessage]) -> list[BaseMessage]:
        # 1. 사용자 질문만 추출 (AI 답변 제외)
        human_messages = [msg for msg in past_messages if isinstance(msg, HumanMessage)]
        logger.info(f"[CONTEXT] 도구 판별용 히스토리: {len(human_messages)}개의 HumanMessage 추출")

        # 2. 과거 질문이 없다면 현재 질문만 반환
        if not human_messages:
            return [HumanMessage(content=user_prompt)]

        # 3. 과거 질문이 있다면 텍스트 하나로 병합
        past_context_text = "\n".join([f"- {msg.content}" for msg in human_messages])

        # 4. 구조화된 단일 프롬프트 생성
        merged_prompt = (
            f"[이전 대화 맥락]\n"
            f"{past_context_text}\n\n"
            f"[현재 질문]\n"
            f"{user_prompt}"
        )

        # 5. Gemma 규칙에 맞춰 1개의 HumanMessage만 반환
        return [HumanMessage(content=merged_prompt)]

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
    async def _process_tool_results(self, response: AIMessage):
        if response.tool_calls:
            logger.info(f"[STEP 3] 도구 실행 파이프라인 진입")
            tool_messages = await self._execute_tool_calls(response.tool_calls)
            return [response] + list(tool_messages)
        else:
            logger.info(f"[STEP 3] 도구 미사용 판단. 일반 대화 처리")
            return []

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
    @staticmethod
    def _build_final_messages(user_prompt: str, tool_results: list, past_messages: list[BaseMessage]) -> list[BaseMessage]:
        processed_messages = []
        for msg in past_messages:
            if isinstance(msg, AIMessage):
                # [참고 자료] 섹션 통째로 날리기 (LLM이 참고자료를 지어내는 할루시네이션 방지)
                clean_content = msg.content.split('[참고 자료]')[0]

                # 새로운 형태의 AIMessage 객체로 복사하여 추가
                processed_messages.append(AIMessage(content=clean_content.strip()))
            else:
                processed_messages.append(msg)

        logger.info(f"[CONTEXT] 최종 답변용 히스토리 정제 완료 ({len(processed_messages)}개)")
        return processed_messages + [HumanMessage(content=user_prompt)] + tool_results

    async def _stream_final_response(self, messages: list[BaseMessage]):
        system_message = SystemMessage(content=self.final_response_prompt)
        final_messages = [system_message] + messages

        async for chunk in self.llm.astream(final_messages):
            if chunk.content:
                yield chunk.content


internal_chat_service = InternalChatService()