from app.schemas import ChatResponse

class SurveyService:

    async def handle(self, user_prompt: str, session_id: str):
        response = {
            "type": "survey_question",
            "data": {
                "text": "간단 설문을 진행하시겠습니까?",
                "buttons": [
                    {
                        "label": "예",
                        "action": "START_SURVEY",
                    },
                    {
                        "label": "아니오",
                        "action": "CANCEL_SURVEY"
                    }
                ]
            },
        }

        yield self._build_response(response)

    async def start_survey(self, session_id: str):
        response = {
            "type": "custom_html",
            "data": {
                "title": "대국민 간단 설문지",
                "subtitle": "생활 패턴 및 기초 건강 실태조사",
                "sections": [
                    {
                        "id": "info",
                        "title": "인적사항",
                        "questions": [
                            {
                                "id": "name",
                                "type": "text",
                                "question": "귀하의 성명은 어떻게 되십니까?",
                                "placeholder": "성함"
                            },
                            {
                                "id": "age",
                                "type": "number",
                                "question": "귀하의 연령은 어떻게 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "세"
                            },
                            {
                                "type": "radio",
                                "id": "gender",
                                "question": "귀하의 성별을 선택해 주십시오.",
                                "options": [
                                    {
                                        "value" : "man",
                                        "label" : "남성"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "여성"
                                    },
                                ]
                            },
                            {
                                "type": "select",
                                "id": "region",
                                "question": "현재 거주하고 계신 지역은 어디입니까?",
                                "options": [
                                    {
                                        "value" : "seoul",
                                        "label" : "서울"
                                    },
                                    {
                                        "value" : "busan",
                                        "label" : "부산"
                                    },
                                ]
                            },
                            {
                                "type": "text",
                                "id": "occupation",
                                "question": "귀하의 직업은 무엇입니까?",
                                "placeholder": "직업",
                            },
                            {
                                "type": "radio",
                                "id": "marital_status",
                                "question": "귀하의 혼인 여부를 선택해주세요.",
                                "options": [
                                    {
                                        "value" : "non_married",
                                        "label" : "미혼"
                                    },
                                    {
                                        "value" : "married",
                                        "label" : "기혼"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "current_cigarette_smoker",
                                "question": "귀하의 현재 흡연 여부를 선택해주세요.",
                                "options": [
                                    {
                                        "value" : "smoking",
                                        "label" : "흡연"
                                    },
                                    {
                                        "value" : "non_smoking",
                                        "label" : "비흡연"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "sex",
                                "question": "최근 1주일 동안 스트레칭, 맨손체조 등의 유연성 운동을 한 날은 며칠입니까?",
                                "options": [
                                    {
                                        "value" : "man",
                                        "label" : "전혀 하지 않음"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "1일"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "2일"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "3일"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "4일"
                                    },
                                    {
                                        "value" : "woman",
                                        "label" : "5일 이상"
                                    },
                                ]
                            },
                        ]
                    },
                ],
            }
        }

        yield self._build_response(response)


    @staticmethod
    def _build_response(data):
        return f"data: {ChatResponse(**data).model_dump_json()}\n\n"

survey_service = SurveyService()