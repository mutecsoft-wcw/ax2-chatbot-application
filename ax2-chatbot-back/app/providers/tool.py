from langchain_core.tools import tool
from pydantic import BaseModel, Field
from .es import chs_raw_guide_retriever, chs_question_guide_retriever, knhanes_raw_guide_retriever, nhip_health_info_retriever
from app.core  import logger

class SearchGuideInput(BaseModel):
    query: str = Field(
        description="검색할 구체적인 키워드나 짧은 문장. (예: '복합표본 가중치 적용법', '개인용 원시자료 변수 규칙')"
    )

def result_formatted(docs) -> str:
    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다. 다른 키워드로 다시 검색해주세요."

    logger.info(docs)

    formatted_results = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "제목 없음")
        content = doc.page_content
        info = f"[문서 {i+1}] {source}\n내용: {content}"
        formatted_results.append(info)

    return "\n\n".join(formatted_results)

@tool("chs_raw_guide_tool", args_schema=SearchGuideInput)
async def chs_raw_guide_tool(query: str) -> str:
    """
    지역사회건강조사(CHS) 2025년 **'원시자료 이용지침서'**의 기술적 내용을 검색합니다.
    통계 분석을 위한 전문적인 가이드가 필요할 때 반드시 이 도구를 사용하세요.

    **주요 포함 내용**
    1. 통계 및 분석: 표본설계(층화, 집락 추출), 가중치(Weights) 계산 및 적용법, 복합표본설계 분석 방법론(분산 추정 등).
    2. 데이터 구조: 자료의 구성(가구용, 개인용), 데이터셋 구조, 변수명(Variable Name) 명명 규칙 및 코드북 체계.
    3. 기술적 지침: 통계 패키지(SAS, SPSS, STATA, R) 활용법, 결측값 처리 기준, 연도별 자료 결합(Merge) 방법.
    4. 조사 개요: 조사 체계, 자료관리 및 정제 과정, 공표 기준 등 분석가가 데이터를 다루기 위해 필수적으로 알아야 하는 정보를 제공합니다.

    단순 설문 문구가 아닌 **'통계 분석 방법'**이나 **'데이터 변수 정의'**에 관한 질문일 때 최적화된 도구입니다.
    """

    docs = await chs_raw_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("chs_question_guide_tool", args_schema=SearchGuideInput)
async def chs_question_guide_tool(query: str) -> str:
    """
    지역사회건강조사(CHS) **'조사문항지침서'**의 내용을 검색합니다.
    설문 문항의 구체적인 정의, 조사 목적, 면접 지침, 응답 분류 기준이 필요할 때 반드시 이 도구를 사용하세요.

    **주요 포함 내용**
    1. 문항별 정의 및 목적: 건강행태(흡연, 음주, 신체활동, 식생활), 만성질환(고혈압, 당뇨병 등), 삶의 질, 정신건강 등 각 조사 항목의 정의와 측정 목적.
    2. 조사 지침: 조사원이 질문을 읽는 방법(문의 요령), 응답 유도시 주의사항, 특정 답변에 대한 판단 기준.
    3. 응답 범주 및 처리: 각 선택지(예/아니오 등)의 상세 설명, 문항 간 건너뛰기(Skip) 로직, 비해당 및 무응답 처리 기준.
    4. 주요 지표 산출 근거: '현재 흡연자'의 정의, '중강도 신체활동'의 예시, '우울감 경험' 조사 시점 등 통계 지표의 기초가 되는 문항별 해설.

    통계 분석 방법론이 아닌, '설문지 문구의 의미', '질문 대상', **'조사 용어의 정의'**에 관한 질문일 때 최적화된 도구입니다.
    """

    docs = await chs_question_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("knhanes_raw_guide_tool", args_schema=SearchGuideInput)
async def knhanes_raw_guide_tool(query: str) -> str:
    """
    국민건강영양조사(KNHANES) **'원시자료 이용지침서'**의 기술적 내용을 검색합니다.
    국가 수준의 건강 및 영양 통계 분석을 위한 전문 가이드가 필요할 때 반드시 이 도구를 사용하세요.

    **주요 포함 내용**
    1. 통계 및 분석: 국가 대표성 확보를 위한 표본 설계(층화계통추출법), 복합표본설계 가중치(Weights) 산출 및 적용법, 분산 추정 방법론.
    2. 조사 영역별 지침:
       - 건강설문조사: 가구 및 개인별 질병 이환, 의료 이용 등
       - 검진조사: 혈압, 혈액검사, 소변검사, 구강검진 등 임상 데이터 측정 기준
       - 영양조사: 24시간 회상법을 통한 식품 및 영양소 섭취량 분석법
    3. 데이터 구조: 데이터셋 구성(가구, 검진, 영양), 변수명(Variable Name) 정의 및 코드북 체계, 연도별 자료 통합(Merge) 및 시계열 분석 방법.
    4. 기술적 지원: SAS, SPSS 전용 분석 코드 예시 및 결측값 처리 지침.

    지역 단위가 아닌 '국가 전체 통계', '임상 검진 데이터 분석', **'식품 섭취 영양 분석'**에 관한 기술적 질문에 최적화된 도구입니다.
    """

    docs = await knhanes_raw_guide_retriever.ainvoke(query)
    return result_formatted(docs)

@tool("nhip_health_info_tool", args_schema=SearchGuideInput)
async def nhip_health_info_tool(query: str) -> str:
    """
    질병관리청 '국가건강정보포털'의 의학 정보를 검색합니다.
    특정 질병의 정의, 증상, 원인, 치료법 등 일반적인 '의학 지식'이나 '건강 상식'을 물어볼 때 사용합니다.
    조사 방법론이나 통계 변수가 아닌, 순수 의학적 가이드가 필요할 때만 사용하세요.
    """

    docs = await nhip_health_info_retriever.ainvoke(query)
    return result_formatted(docs)


tools = [
    chs_raw_guide_tool,
    chs_question_guide_tool,
    knhanes_raw_guide_tool,
    nhip_health_info_tool,
]