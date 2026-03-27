import logging
import sys

# 로그 출력 형식 설정 (시각 - 이름 - 레벨 - 메시지)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logger():
    logger = logging.getLogger("app_logger")  # 로거 인스턴스 이름
    logger.setLevel(logging.INFO)  # 기본 로그 레벨 설정

    # 핸들러 설정 (콘솔 출력용)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stream_handler)

    # 파일 출력용 핸들러 추가
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    # logger.addHandler(file_handler)

    return logger


logger = setup_logger()
