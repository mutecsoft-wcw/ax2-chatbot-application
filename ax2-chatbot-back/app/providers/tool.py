from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from datetime import datetime

from app.core import settings
from .es import search_guide_documents, search_health_info, search_indicator_data, _indicator_result_formatted

CURRENT_YEAR = datetime.now().year

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
    year: Optional[int] = Field(
        default=None,
        description=(
            "Converts specific years (e.g., '2023') or relative terms (e.g., 'last year', 'this year', 'next year') "
            f"mentioned in the user's query into a 4-digit integer. The baseline for the current year is {CURRENT_YEAR}. "
            "[Important Rule]: When calling multiple tools in parallel for a single query, if a year (e.g., '2025') "
            "is mentioned at the beginning or within the context, apply that same year to the 'year' parameter "
            "of all relevant tools. "
            "Return null only if there is no mention of a year throughout the entire query."
        )
    )

class HealthInfoSearchInput(BaseModel):
    query: str = Field(
        description=(
            "A specific single keyword or short phrase to search. "
            "[CRITICAL RULE 1]: NEVER call this tool for simple greetings (e.g., '안녕하세요', '안녕', '반가워'), gratitude, or casual conversation. If the user is just greeting, DO NOT invoke any tools. "
            "[CRITICAL RULE 2]: If you need to compare or simultaneously search two or more diseases or concepts, "
            "NEVER combine them into a single query. "
            "You MUST split the question and call this tool multiple times independently (Parallel Calling). "
            "(e.g., User asks: '고혈압과 당뇨의 증상' -> Call 1: query='고혈압 증상', Call 2: query='당뇨 증상')"
        )
    )

class SearchIndicatorInput(BaseModel):
    query: str = Field(
        description=(
            "A specific indicator name, disease, or health behavior to search for. (e.g., '당뇨병 유병률', '현재흡연율', '걷기실천율') "
            "[CRITICAL RULE 1]: NEVER call this tool for simple greetings. "
            "[CRITICAL RULE 2]: If you need to compare multiple indicators, regions, or years, "
            "NEVER combine them into a single query. "
            "You MUST split the question and call this tool multiple times independently (Parallel Calling). "
            "(e.g., User asks: '2023년과 2024년 고혈압 유병률' -> Call 1: query='고혈압 유병률', year=2023 / Call 2: query='고혈압 유병률', year=2024)"
        )
    )
    year: Optional[int] = Field(
        default=None,
        description=(
            "Converts specific years (e.g., '2023') or relative terms (e.g., 'last year', 'this year', 'next year') "
            f"mentioned in the user's query into a 4-digit integer. The baseline for the current year is {CURRENT_YEAR}. "
            "[Important Rule]: When calling multiple tools in parallel for a single query, if a year (e.g., '2025') "
            "is mentioned at the beginning or within the context, apply that same year to the 'year' parameter "
            "of all relevant tools. "
            "Return null only if there is no mention of a year throughout the entire query."
        )
    )

# 지역사회건강조사 원시자료 이용지침서
@tool("chs_raw_guide_tool", args_schema=SearchGuideInput)
async def chs_raw_guide_tool(query: str, year: Optional[int] = None) -> str:
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
    return await search_guide_documents(
        index_name=settings.elasticsearch["indices"]["chs_raw_guide_index"],
        query=query,
        year=year
    )

# 지역사회건강조사 조사문항지침서
@tool("chs_question_guide_tool", args_schema=SearchGuideInput)
async def chs_question_guide_tool(query: str, year: Optional[int] = None) -> str:
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

    return await search_guide_documents(
        index_name=settings.elasticsearch["indices"]["chs_question_guide_index"],
        query=query,
        year=year
    )

# 지역사회건강조사 조사표
@tool("chs_form_tool", args_schema=SearchGuideInput)
async def chs_form_tool(query: str, year: Optional[int] = None) -> str:
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

    return await search_guide_documents(
        index_name=settings.elasticsearch["indices"]["chs_form_index"],
        query=query,
        year=year
    )

# 국민건강영양조사 원시자료 이용지침서
@tool("knhanes_raw_guide_tool", args_schema=SearchGuideInput)
async def knhanes_raw_guide_tool(query: str, year: Optional[int] = None) -> str:
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

    return await search_guide_documents(
        index_name=settings.elasticsearch["indices"]["knhanes_raw_guide_index"],
        query=query,
        year=year
    )

# 질병관리청 국가건강정보
@tool("nhip_health_info_tool", args_schema=HealthInfoSearchInput)
async def nhip_health_info_tool(query: str) -> str:
    """
    Search for medical information from the KDCA 'National Health Information Portal (국가건강정보포털)'.
    You MUST use this tool to ask about general '의학 지식' (medical knowledge) or '건강 상식' (health common sense), such as the 정의 (definition), 증상 (symptoms), 원인 (causes), and 치료법 (treatments) of a specific disease.

    [USAGE CONDITION]: You MUST use this tool ONLY when pure medical guidelines are needed.
    DO NOT use this tool for survey methodologies (조사 방법론), statistical variables (통계 변수), or data structures.
    [CRITICAL]: NEVER use this tool for general chat, greetings ('안녕', '안녕하세요'), or non-health related queries.
    """

    return await search_health_info(
        index_name=settings.elasticsearch["indices"]["nhip_health_info_index"],
        query=query
    )

# 지역사회건강조사 지표데이터
@tool("chs_indicator_tool", args_schema=SearchIndicatorInput)
async def chs_indicator_tool(query: str, year: Optional[int] = None) -> str:
    """
    [OBJECTIVE]
    Retrieve actual statistical figures (percentages, rates, prevalence) from the Community Health Survey (CHS).
    This tool performs a vector search directly against the exact 'indicator_name' field in Elasticsearch.

    [INPUT GUIDANCE]
    The `query` MUST be highly optimized to match the official indicator names. Align the `query` closely with these actual examples:
    - Smoking (흡연): "현재흡연율", "담배제품 현재사용율", "담배제품 현재사용자의 금연시도율", "담배제품 현재 미사용자의 직장실내 간접흡연 노출률"
    - Drinking (음주): "월간음주율", "고위험음주율", "연간음주자의 고위험음주율", "자동차 또는 오토바이 운전자의 연간 음주운전 경험률"
    - Physical/Obesity (신체활동/비만): "걷기 실천율", "중강도 이상 신체활동 실천율", "건강생활실천율", "비만율(자가보고)", "연간 체중조절 시도율"
    - Nutrition (영양): "아침 식사 실천율", "영양표시 인지율", "영양표시 활용률"
    - Mental Health (정신건강): "스트레스 인지율", "연간 우울감 경험률", "우울증상유병률", "삶의 질 지수 (EQ-5D Index)"
    - Chronic Disease (만성질환): "고혈압 진단 경험률 (30세 이상)", "당뇨병 진단 경험률 (30세 이상)", "고혈압 진단 경험자의 치료율 (30세 이상)", "혈압수치 인지율"
    - Safety/Hygiene (안전/위생): "운전자석 안전벨트 착용률", "외출 후 손 씻기 실천율", "비누, 손 세정제 사용률", "어제 점심식사 후 칫솔질 실천율"

    [WHEN TO USE]
    - When the user specifically asks for numerical statistics, percentages (%), or indicator results.
    - Questions like: "OO율이 얼마야?", "OO 지표 통계 알려줘", "What is the rate of..."

    [MATCHING RULE]
    - NEVER include conversational fluff in the `query`.
    - If the user asks about Diabetes or Hypertension rates, include the age qualifier "(30세 이상)" in the query if appropriate to maximize vector similarity.
    """

    MIN_YEAR = 2019

    target_year = year if year is not None else (CURRENT_YEAR - 1)

    # 요청한 연도가 올해(또는 그 이후)라면, 가장 최신 데이터인 작년으로 덮어씌웁니다.
    if target_year >= CURRENT_YEAR:
        target_year = CURRENT_YEAR - 1

    # 만약 요청 연도가 너무 과거라면 즉시 차단
    if target_year < MIN_YEAR:
        return f"[데이터 없음] 지역사회건강조사 지표는 {MIN_YEAR}년부터 제공됩니다. {target_year}년은 조회할 수 없습니다."

    # 인덱스 타겟팅 및 검색 실행
    target_index = f"chs-indicator-vector-{target_year}"

    docs = await search_indicator_data(
        index_name=target_index,
        query=query
    )

    # 에러 발생 시 처리
    if isinstance(docs, str):
        return docs

    # 검색 결과가 하나도 없는 경우
    if len(docs) == 0:
        return f"'{query}'와 관련하여 {target_year}년 통계 데이터를 찾지 못했습니다."

    # 정상적으로 데이터를 찾은 경우 텍스트로 포맷팅
    result_str = _indicator_result_formatted(docs)

    # 사용자가 원래 요청했던 연도와 실제 조회된 연도(작년)가 다를 때만 안내 문구 추가
    if year and year != target_year:
        prefix = f"{year}년 데이터가 아직 구축되지 않아, 가장 최신인 {target_year}년 자료를 대신 보여드립니다.\n\n"
        return f"{prefix}{result_str}"

    # 모든 연도를 다 뒤졌는데도 끝내 못 찾았을 경우
    return result_str


tools = [
    chs_raw_guide_tool,
    chs_question_guide_tool,
    chs_form_tool,
    knhanes_raw_guide_tool,
    nhip_health_info_tool,
    chs_indicator_tool
]
