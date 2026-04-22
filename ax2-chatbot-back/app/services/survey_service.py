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
                                "placeholder": "만 나이",
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
                                        "value" : "미혼",
                                        "label" : "미혼"
                                    },
                                    {
                                        "value" : "기혼",
                                        "label" : "기혼"
                                    },
                                    {
                                        "value" : "기타(이혼/사별)",
                                        "label" : "기타(이혼/사별)"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "current_cigarette_smoker",
                                "question": "귀하의 현재 흡연 여부를 선택해주세요.",
                                "options": [
                                    {
                                        "value" : "흡연",
                                        "label" : "흡연"
                                    },
                                    {
                                        "value" : "비흡연",
                                        "label" : "비흡연"
                                    },
                                ]
                            },
                            {
                                "id": "height_cm",
                                "type": "number",
                                "question": "귀하의 신장(cm)은 어떻게 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "cm"
                            },
                            {
                                "id": "weight_kg",
                                "type": "number",
                                "question": "귀하의 체중(kg)은 어떻게 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "kg"
                            },
                            {
                                "id": "vigorous_days_per_week",
                                "type": "number",
                                "question": "최근 1주일 동안, 평소보다 몸이 훨씬 힘들거나 숨이 많이 가쁜 격렬한 신체활동을 10분 이상 하신 날은 며칠입니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "vigorous_hours",
                                "type": "number",
                                "question": "평균적으로 격렬한 운동을 한 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "vigorous_minutes",
                                "type": "number",
                                "question": "평균적으로 격렬한 운동을 한 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "id": "moderate_days_per_week",
                                "type": "number",
                                "question": "최근 1주일 동안, 땀이 날 정도의 중강도 운동을 10분 이상 하신 날은 며칠입니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "moderate_hours",
                                "type": "number",
                                "question": "평균적으로 중강도 운동을 하는 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "moderate_minutes",
                                "type": "number",
                                "question": "평균적으로 중강도 운동을 하는 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "id": "walking_days_per_week",
                                "type": "number",
                                "question": "최근 1주일 동안 출퇴근 외의 걷기 운동을 하신 날은 며칠입니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "walking_hours",
                                "type": "number",
                                "question": "평균적으로 걷기 운동을 한 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "walking_minutes",
                                "type": "number",
                                "question": "평균적으로 걷기 운동을 한 시간은 얼마나 되십니까?",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "type": "radio",
                                "id": "flexibility_exercise_last_week",
                                "question": "최근 1주일 동안 스트레칭, 맨손체조 등의 유연성 운동을 한 날은 며칠입니까?",
                                "options": [
                                    {
                                        "value" : "전혀 하지 않음",
                                        "label" : "전혀 하지 않음"
                                    },
                                    {
                                        "value" : "매우 가끔",
                                        "label" : "매우 가끔"
                                    },
                                    {
                                        "value" : "가끔",
                                        "label" : "가끔"
                                    },
                                    {
                                        "value" : "자주",
                                        "label" : "자주"
                                    },
                                    {
                                        "value" : "매우 자주",
                                        "label" : "매우 자주"
                                    },
                                    {
                                        "value" : "매일",
                                        "label" : "매일"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "info2",
                        "title": "인적사항2",
                        "questions": [
                            {
                                "id": "name2",
                                "type": "text",
                                "question": "귀하의 성명은 어떻게 되십니까?2",
                                "placeholder": "성함"
                            },
                            {
                                "id": "age",
                                "type": "number2",
                                "question": "귀하의 연령은 어떻게 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "세"
                            },
                            {
                                "type": "radio",
                                "id": "gender2",
                                "question": "귀하의 성별을 선택해 주십시오.2",
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
                                "id": "region2",
                                "question": "현재 거주하고 계신 지역은 어디입니까?2",
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
                                "id": "occupation2",
                                "question": "귀하의 직업은 무엇입니까?2",
                                "placeholder": "직업",
                            },
                            {
                                "type": "radio",
                                "id": "marital_status2",
                                "question": "귀하의 혼인 여부를 선택해주세요.2",
                                "options": [
                                    {
                                        "value" : "미혼",
                                        "label" : "미혼"
                                    },
                                    {
                                        "value" : "기혼",
                                        "label" : "기혼"
                                    },
                                    {
                                        "value" : "기타(이혼/사별)",
                                        "label" : "기타(이혼/사별)"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "current_cigarette_smoker2",
                                "question": "귀하의 현재 흡연 여부를 선택해주세요.2",
                                "options": [
                                    {
                                        "value" : "흡연",
                                        "label" : "흡연"
                                    },
                                    {
                                        "value" : "비흡연",
                                        "label" : "비흡연"
                                    },
                                ]
                            },
                            {
                                "id": "height_cm2",
                                "type": "number",
                                "question": "귀하의 신장(cm)은 어떻게 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "cm"
                            },
                            {
                                "id": "weight_kg2",
                                "type": "number",
                                "question": "귀하의 체중(kg)은 어떻게 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 999,
                                "suffix": "kg"
                            },
                            {
                                "id": "vigorous_days_per_week2",
                                "type": "number",
                                "question": "최근 1주일 동안 숨을 헐떡일 정도의 격렬한 운동을 한 날은 며칠입니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "vigorous_hours2",
                                "type": "number",
                                "question": "평균적으로 격렬한 운동을 한 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "vigorous_minutes2",
                                "type": "number",
                                "question": "평균적으로 격렬한 운동을 한 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "id": "moderate_days_per_week2",
                                "type": "number",
                                "question": "최근 1주일 동안 땀이 날 정도의 중강도 운동을 한 날은 며칠입니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "moderate_hours2",
                                "type": "number",
                                "question": "평균적으로 중강도 운동을 하는 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "moderate_minutes2",
                                "type": "number",
                                "question": "평균적으로 중강도 운동을 하는 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "id": "walking_days_per_week2",
                                "type": "number",
                                "question": "최근 1주일 동안 출퇴근 외의 걷기 운동을 한 날은 며칠입니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 7,
                                "suffix": "일"
                            },
                            {
                                "id": "walking_hours2",
                                "type": "number",
                                "question": "평균적으로 걷기 운동을 한 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 24,
                                "suffix": "시간"
                            },
                            {
                                "id": "walking_minutes2",
                                "type": "number",
                                "question": "평균적으로 걷기 운동을 한 시간은 얼마나 되십니까?2",
                                "placeholder": "",
                                "min" : 0,
                                "max" : 60,
                                "suffix": "분"
                            },
                            {
                                "type": "radio",
                                "id": "flexibility_exercise_last_week2",
                                "question": "최근 1주일 동안 스트레칭, 맨손체조 등의 유연성 운동을 한 날은 며칠입니까?2",
                                "options": [
                                    {
                                        "value" : "전혀 하지 않음",
                                        "label" : "전혀 하지 않음"
                                    },
                                    {
                                        "value" : "매우 가끔",
                                        "label" : "매우 가끔"
                                    },
                                    {
                                        "value" : "가끔",
                                        "label" : "가끔"
                                    },
                                    {
                                        "value" : "자주",
                                        "label" : "자주"
                                    },
                                    {
                                        "value" : "매우 자주",
                                        "label" : "매우 자주"
                                    },
                                    {
                                        "value" : "매일",
                                        "label" : "매일"
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