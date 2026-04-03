import yaml
from pathlib import Path
from .logger import logger


class Settings:
    def __init__(self):
        # 프로젝트 루트의 config.yml 로드
        config_path = Path(__file__).parent.parent.parent / "config.yml"

        # 파일이 없으면 중단
        if not config_path.exists():
            logger.critical(f"설정 파일을 찾을 수 없습니다.", config_path)
            raise FileNotFoundError(f"Configuration file not found at {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:

            config = yaml.safe_load(f)

            # 필수 설정 값이 없으면 중단
            try:
                self.llm = config["llm"]
                self.embedding = config["embedding"]
                self.elasticsearch = config["elasticsearch"]
                self.base_url = self.llm["base_url"].rstrip("/")
                self.cors_url = config["cors_url"]
                self.redis = config["redis"]

                logger.info("설정 파일 로드 성공.")

            except KeyError as e:
                logger.critical(f"필수 설정 항목이 누락되었습니다.: {e}")
                raise


settings = Settings()
