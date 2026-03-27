import json

from app.core import logger
from app.schemas import ChatResponse, GUIDE_DOCS_TOOLS
from app.providers import llm_config, llm_model
from app.utils.file_utils import load_prompt_file
from app.services.search_service import search_service


class ChatService:
    def __init__(self):
        self.llm = llm_model
        self.llm_config = llm_config
        self.search_service = search_service

        self.tools = GUIDE_DOCS_TOOLS

        # 프롬프트 로드
        self.tool_router_prompt = load_prompt_file("tool-router-prompt-kor.txt")
        self.final_response_prompt = load_prompt_file("public-guide.txt")

        # 도구 이름과 실행할 함수를 매핑 (개방-폐쇄 원칙 적용)
        self.tool_handlers = {
            "search_guide_docs": self.search_service.search_guide_docs
        }

    async def get_chat_response(self, user_prompt: str):
        try:
            logger.info(f"[STEP 1] 대화 요청 수신: {user_prompt[:50]}...")

            # 1. 메시지 초기화
            initial_messages = self._prepare_initial_messages(user_prompt)

            # 2. 도구 호출 여부 판단 및 실행
            logger.info(f"[STEP 2] LLM 도구 호출 여부 판단 시작")
            context_augmented_messages = await self._router_tool(initial_messages)

            # 3. 최종 답변 생성 및 스트리밍
            logger.info(f"[STEP 5] 최종 답변 스트리밍 시작")
            async for chunk in self._stream_final_response(context_augmented_messages):
                yield chunk

        except Exception as e:
            logger.error(f"[CRITICAL ERROR] {str(e)}", exc_info=True)
            error_response = ChatResponse(text="서비스 처리 중 오류가 발생했습니다.")
            yield f"data: {error_response.model_dump_json()}\n\n"

    def _prepare_initial_messages(self, user_prompt: str) -> list[dict]:
        return [
            {"role": "system", "content": self.tool_router_prompt},
            {"role": "user", "content": user_prompt}
        ]

    async def _router_tool(self, messages: list[dict]) -> list[dict]:
        response = await self.llm.chat.completions.create(
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            **self.llm_config
        )

        assistant_msg = response.choices[0].message

        # 도구 호출이 있는 경우
        if assistant_msg.tool_calls:
            logger.info(f"[STEP 3] 도구 호출 감지: {len(assistant_msg.tool_calls)}건")
            # 모델의 응답 메시지를 히스토리에 추가
            messages.append(assistant_msg.model_dump(exclude_none=True))

            # 실제 도구 실행 루프
            messages = await self._execute_tool_calls(assistant_msg.tool_calls, messages)

            # 도구 결과가 추가되었으므로, 최종 답변을 위해 시스템 프롬프트(페르소나) 교체
            logger.info(f"[STEP 4] 전문가 페르소나 적용 및 최종 답변 구성")
            messages[0] = {"role": "system", "content": self.final_response_prompt}

        else:
            logger.info(f"[STEP 3] 도구 미사용 (일반 대화)")

        return messages

    async def _execute_tool_calls(self, tool_calls, messages: list[dict]) -> list[dict]:
        for i, tool_call in enumerate(tool_calls):
            function_name = tool_call.function.name

            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                logger.error(f"[ERROR] 도구 인자 JSON 파싱 실패: {tool_call.function.arguments}")
                tool_result = "인자 파싱 오류: 올바른 JSON 형식이 아닙니다."
            else:
                logger.info(f"[STEP 3-{i+1}] 도구 실행: {function_name}(args={args})")

                # 핸들러 매핑에서 함수 가져오기
                handler = self.tool_handlers.get(function_name)
                if handler:
                    # 핸들러 실행 (비동기)
                    tool_result = await handler(**args)
                    logger.info(f"[STEP 3-RESULT] {i+1}번 도구 실행 완료 (결과 길이: {len(str(tool_result))}자)")
                else:
                    logger.warning(f"[WARNING] 알 수 없는 도구 호출: {function_name}")
                    tool_result = "해당 기능을 수행할 수 있는 도구를 찾을 수 없습니다."

            # 도구 실행 결과를 메시지 리스트에 추가
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(tool_result)
            })

        return messages

    async def _stream_final_response(self, messages: list[dict]):
        stream = await self.llm.chat.completions.create(
            messages=messages,
            stream=True,
            **self.llm_config
        )

        full_content = []
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                text_chunk = chunk.choices[0].delta.content
                full_content.append(text_chunk)
                yield f"data: {ChatResponse(text=text_chunk).model_dump_json()}\n\n"

        logger.info(f"[STEP 6] 스트리밍 종료 (총 응답 길이: {len(''.join(full_content))}자)")


chat_service = ChatService()