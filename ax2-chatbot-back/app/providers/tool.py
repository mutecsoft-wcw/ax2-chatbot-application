from langchain_core.tools import tool
from pydantic import BaseModel, Field
from .es import (
    chs_raw_guide_retriever,
    chs_question_guide_retriever,
    knhanes_raw_guide_retriever,
    nhip_health_info_retriever,
    chs_form_retriever
)
from app.core  import logger

class SearchGuideInput(BaseModel):
    query: str = Field(
        description=(
            "A specific single keyword or short phrase to search. "
            "[CRITICAL RULE 1]: NEVER call this tool for simple greetings (e.g., '안녕하세요', '안녕', '반가워'), gratitude, or casual conversation. If the user is just greeting, DO NOT invoke any tools. "
            "[CRITICAL RULE 2]: If you need to compare or simultaneously search two or more documents, concepts, or years, "
            "NEVER combine them into a single query. "
            "You MUST split the question and call this tool multiple times independently (Parallel Calling). "
            "(e.g., User asks: 'A지침서와 B지침서의 목적' -> Call 1: query='A지침서 목적', Call 2: query='B지침서 목적')"
        )
    )

def result_formatted(docs) -> str:
    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다. 다른 키워드로 다시 검색해주세요."

    formatted_results = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "제목 없음")
        content = doc.page_content
        info = f"[문서 {i+1}] {source}\n내용: {content}"

        logger.info(info)

        formatted_results.append(info)

    return "\n\n".join(formatted_results)

@tool("chs_raw_guide_tool", args_schema=SearchGuideInput)
async def chs_raw_guide_tool(query: str) -> str:
    """
    Search the technical contents of the 2025 Community Health Survey (CHS, 지역사회건강조사) **'Raw Data Usage Guide (원시자료 이용지침서)'**.
    You MUST use this tool when a professional guide for statistical analysis or data handling is required.

    **[Key Contents]**
    1. Statistics & Analysis: 표본설계 (층화, 집락 추출), 가중치 (Weights) calculation & application, 복합표본설계 분석 방법론 (분산 추정 등).
    2. Data Structure: 자료의 구성 (가구용, 개인용), dataset structure, 변수명 (Variable Name) rules, and 코드북 (Codebook) 체계.
    3. Technical Guidelines: How to use 통계 패키지 (SAS, SPSS, STATA, R), 결측값 처리 기준, 연도별 자료 결합 (Merge) 방법.
    4. Survey Overview: 조사 체계, 자료관리 및 정제 과정, 공표 기준 등 (essential background for data analysts).

    [USAGE CONDITION]: Use this tool ONLY for technical queries regarding **'통계 분석 방법' (Statistical analysis methods)** or **'데이터 변수 정의' (Data variable definitions)**.
    DO NOT use this tool for simple survey question meanings.
    """

    docs = await chs_raw_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("chs_question_guide_tool", args_schema=SearchGuideInput)
async def chs_question_guide_tool(query: str) -> str:
    """
    Search the contents of the Community Health Survey (CHS, 지역사회건강조사) **'Survey Questionnaire Guide (조사문항지침서)'**.
    You MUST use this tool when you need specific definitions of survey questions, 조사 목적 (survey purpose), 면접 지침 (interview guidelines), or 응답 분류 기준.

    **[Key Contents]**
    1. Definitions & Purpose per Question: 건강행태 (흡연, 음주, 신체활동, 식생활), 만성질환 (고혈압, 당뇨병 등), 삶의 질, 정신건강, and the measurement purpose of each item.
    2. Interview Guidelines: 조사 지침, how interviewers should read questions (문의 요령), precautions for inducing responses, and 판단 기준 for specific answers.
    3. Response Categories & Processing: Detailed explanations of choices, 문항 간 건너뛰기 (Skip logic), and processing criteria for 비해당 (Not Applicable) and 무응답 (Non-response).
    4. Basis for Key Indicators: Definitions of '현재 흡연자', examples of '중강도 신체활동', timing for '우울감 경험', and question-level explanations (문항별 해설).

    [USAGE CONDITION]: This tool is OPTIMIZED for questions about '설문지 문구의 의미' (Meaning of survey text), '질문 대상' (Target respondents), and **'조사 용어의 정의' (Definitions of survey terms)**.
    DO NOT use this tool for statistical analysis methodologies or data structures (use `chs_raw_guide_tool` instead).
    """

    docs = await chs_question_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("chs_form_tool", args_schema=SearchGuideInput)
async def chs_form_tool(query: str) -> str:
    """
    Search the exact contents of the Community Health Survey (CHS, 지역사회건강조사) 'Survey Form / Questionnaire (조사표 / 설문지)'.
    You MUST use this tool to find the exact phrasing of survey questions, response choices (객관식 보기/선택지), and skip logic (건너뛰기/비해당 조건).

    [Key Contents]
    1. Household Survey (가구조사): Questions asked to the household representative, such as 가구 유형 (Household type), 기초생활 수급 여부, 가구 총 소득, and 치매환자 동거 여부.
    2. Individual Survey (개인조사): The actual questions asked to individuals covering areas like 건강행태 (흡연, 음주, 신체활동), 이환 (고혈압, 당뇨병 등), 정신건강, 구강건강, 사고 및 중독, and 보건기관 이용.
    3. Options & Logic (선택지 및 설문 구조): The exact numbering of multiple-choice options (e.g., ① 예, ② 아니오, 1~10점 척도), measurement units (시간, 분, 잔, 개비), and routing instructions (e.g., [3번 문항으로], ⑧ 비해당).

    [USAGE CONDITION]: You MUST use this tool ONLY when you need to know "설문지에서 정확히 어떻게 물어보았는지" (How the question was exactly asked) or "객관식 보기가 무엇인지" (What the options are).
    DO NOT use this tool for detailed definitions of survey terms (use `chs_question_guide_tool`) or statistical data analysis (use `chs_raw_guide_tool`).
    """

    docs = await chs_form_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("knhanes_raw_guide_tool", args_schema=SearchGuideInput)
async def knhanes_raw_guide_tool(query: str) -> str:
    """
    Search the technical contents of the Korea National Health and Nutrition Examination Survey (KNHANES, 국민건강영양조사) **'Raw Data Usage Guide (원시자료 이용지침서)'**.
    You MUST use this tool when you need a professional guide for national-level (국가 수준) health and nutrition statistical analysis.

    **[Key Contents]**
    1. Statistics & Analysis: 표본 설계 (층화계통추출법) for national representativeness, 복합표본설계 가중치 (Weights) calculation & application, and 분산 추정 방법론.
    2. Domain-Specific Guidelines (조사 영역별 지침):
       - Health Questionnaire (건강설문조사): 가구 및 개인별 질병 이환, 의료 이용 등.
       - Examination (검진조사): 임상 데이터 측정 기준 including 혈압, 혈액검사, 소변검사, 구강검진.
       - Nutrition (영양조사): 식품 및 영양소 섭취량 분석법 using 24시간 회상법.
    3. Data Structure: 데이터셋 구성 (가구, 검진, 영양), 변수명 (Variable Name) definitions & 코드북 (Codebook) 체계, 연도별 자료 통합 (Merge) & 시계열 분석 방법.
    4. Technical Support: SAS, SPSS 전용 분석 코드 예시 and 결측값 처리 지침.

    [USAGE CONDITION]: This tool is OPTIMIZED for technical queries regarding '국가 전체 통계' (National overall statistics), '임상 검진 데이터 분석' (Clinical exam data analysis), and **'식품 섭취 영양 분석' (Food & nutrition intake analysis)**.
    DO NOT use this tool for regional-level data (use `chs_raw_guide_tool` instead).
    """

    docs = await knhanes_raw_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("nhip_health_info_tool", args_schema=SearchGuideInput)
async def nhip_health_info_tool(query: str) -> str:
    """
    Search for medical information from the KDCA 'National Health Information Portal (국가건강정보포털)'.
    You MUST use this tool to ask about general '의학 지식' (medical knowledge) or '건강 상식' (health common sense), such as the 정의 (definition), 증상 (symptoms), 원인 (causes), and 치료법 (treatments) of a specific disease.

    [USAGE CONDITION]: You MUST use this tool ONLY when pure medical guidelines are needed.
    DO NOT use this tool for survey methodologies (조사 방법론), statistical variables (통계 변수), or data structures.
    [CRITICAL]: NEVER use this tool for general chat, greetings ('안녕', '안녕하세요'), or non-health related queries.
    """

    docs = await nhip_health_info_retriever.ainvoke(query)
    return result_formatted(docs)


tools = [
    chs_raw_guide_tool,
    chs_question_guide_tool,
    chs_form_tool,
    knhanes_raw_guide_tool,
    nhip_health_info_tool,
]