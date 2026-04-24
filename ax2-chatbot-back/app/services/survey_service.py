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
                        "title": "기본 정보와 신체 지표",
                        "questions": [
                            {
                                "id": "name",
                                "type": "text",
                                "question": "귀하의 성명은 어떻게 되십니까?",
                                "placeholder": "성명"
                            },
                            {
                                "id": "age",
                                "type": "number",
                                "question": "귀하의 연령은 어떻게 되십니까?",
                                "placeholder": "만",
                                "min" : 0,
                                "max" : 200,
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
                                "type": "select",
                                "id": "occupation",
                                "question": "귀하의 직업은 무엇입니까?",
                                "options": [
                                    {
                                        "value" : "doctor",
                                        "label" : "의사"
                                    },
                                    {
                                        "value" : "teacher",
                                        "label" : "선생"
                                    },
                                    {
                                        "value" : "student",
                                        "label" : "학생"
                                    },
                                ]
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
                                "type": "text",
                                "question": "귀하의 신장(cm)은 어떻게 되십니까?",
                                "placeholder": "",
                                "suffix": "cm"
                            },
                            {
                                "id": "weight_kg",
                                "type": "text",
                                "question": "귀하의 체중(kg)은 어떻게 되십니까?",
                                "placeholder": "",
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
                    }
                ],
            }
        }
        
        yield self._build_response(response)
        
    async def improvement_survey(self, session_id: str):
        response = {
            "type": "improvement_survey_html",
            "data": {
                "title": "대국민 건강 개선 설문지",
                "subtitle": "개인 건강 및 생활습관",
                "sections": [
                    {
                        "id": "hygiene",
                        "title": "개인 위생",
                        "questions": [
                            {
                                "id": "brushed_before_bed_yesterday",
                                "type": "radio",
                                "question": "어제 하루동안 칫솔질 실천 여부 _저녁식사 후 또는 잠자기 전에",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "어제 저녁식사 또는 잠자지 않음"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "handwashing_after_using_restroom",
                                "question": "화장실 다녀온 후 손 씻기 실천 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "항상 씻었다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "자주 씻었다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "가끔 씻었다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "거의 씻지 않았다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "usage_of_soap_or_hand_sanitizer",
                                "question": "비누, 손 세정제 사용 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "항상 사용한다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "자주 사용한다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "가끔 사용한다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "거의 사용하지 않는다"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "전혀 사용하지 않는다"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "healthIntent",
                        "title": "건강개선 의지",
                        "questions": [
                            {
                                "id": "plan_to_quit_smoking",
                                "type": "radio",
                                "question": "금연 계획 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "현재로서는 전혀 금연할 생각이 없다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "향후 6개월 이내에 금연할 계획이 있다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "향후 1개월 이내에 금연할 계획이 있다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "현재 금연을 실천하고 있으며, 그 기간이 6개월 미만이다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "plan_to_reduce_or_quit_drinking",
                                "question": "절주 또는 금주계획 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "현재로서는 전혀 절주 또는 금주할 생각이 없다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "향후 6개월 이내에 절주 또는 금주할 계획이 있다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "향후 1개월 이내에 절주 또는 금주할 계획이 있다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "현재 절주 또는 금주를 실천하고 있으며, 그 기간이 6개월 미만이다"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "현재 절주 또는 금주를 실천하고 있으며, 그 기간이 6개월 이상이다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "annual_unmet_dental_care_need",
                                "question": "연간 미충족의료여부(치과)",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "치과진료(검사 또는 치료)가 필요한 적이 없었다"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "healthLiteracyScore",
                        "title": "건강지식",
                        "questions": [
                            {
                                "id": "cpr_awareness",
                                "type": "radio",
                                "question": "심폐소생술 인지 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "aware_of_total_cholesterol_level",
                                "question": "총 콜레스테롤 인지 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "sleep_quality",
                                "question": "전반적인 수면의 질",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "매우 좋음"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "상당히 좋음"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "상당히 나쁨"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "매우 나쁨"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "safetyAwareness",
                        "title": "안전의식",
                        "questions": [
                            {
                                "id": "seatbelt_driver",
                                "type": "radio",
                                "question": "자동차 안전벨트 착용 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "운전을 하지 않는다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "전혀 매지 않는다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "거의 매지 않는 편이다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "가끔 매는 편이다"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "대체로 매는 편이다"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "항상 맨다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "motorcycle_helmet_use",
                                "question": "오토바이 헬맷 착용 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "운전을 하지 않는다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "전혀 착용하지 않는다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "거의 착용하지 않는 편이다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "가끔 착용하는 편이다"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "대체로 착용하는 편이다"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "항상 착용한다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "bicycle_helmet_use",
                                "question": "자전거 헬맷 착용 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "자전거를 타지 않는다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "전혀 착용하지 않는다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "거의 착용하지 않는 편이다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "가끔 착용하는 편이다"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "대체로 착용하는 편이다"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "항상 착용한다"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "mentalHealth",
                        "title": "정신건강",
                        "questions": [
                            {
                                "id": "stress_level",
                                "type": "radio",
                                "question": "스트레스 수준",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "대단히 많이 느낀다"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "많이 느끼는 편이다"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "조금 느끼는 편이다"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "거의 느끼지 않는다"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "depressive_mood_experience",
                                "question": "우울감 경험 여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "suicidal_ideation",
                                "question": "자살생각 경험여부",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "예"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "아니오"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "id": "socialInteraction",
                        "title": "타인과의 접점",
                        "questions": [
                            {
                                "id": "contact_frequency_with_relatives",
                                "type": "radio",
                                "question": "친척과의 연락 빈도",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "한 달에 1번 미만"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "한 달에 1번"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "한 달에 2~3번"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "일주일에 1번"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "일주일에 2~3번"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "일주일에 4번 이상"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "contact_frequency_with_neighbors",
                                "question": "이웃과의 연락 빈도",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "한 달에 1번 미만"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "한 달에 1번"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "한 달에 2~3번"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "일주일에 1번"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "일주일에 2~3번"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "일주일에 4번 이상"
                                    },
                                ]
                            },
                            {
                                "type": "radio",
                                "id": "contact_frequency_with_friends",
                                "question": "친구와의 연락 빈도",
                                "options": [
                                    {
                                        "value" : 1,
                                        "label" : "한 달에 1번 미만"
                                    },
                                    {
                                        "value" : 2,
                                        "label" : "한 달에 1번"
                                    },
                                    {
                                        "value" : 3,
                                        "label" : "한 달에 2~3번"
                                    },
                                    {
                                        "value" : 4,
                                        "label" : "일주일에 1번"
                                    },
                                    {
                                        "value" : 5,
                                        "label" : "일주일에 2~3번"
                                    },
                                    {
                                        "value" : 6,
                                        "label" : "일주일에 4번 이상"
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