import yaml
from pathlib import Path

class Settings:
    def __init__(self):
        # 프로젝트 루트의 config.yml 로드
        config_path = Path(__file__).parent.parent.parent / "config.yml"
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.llm = config["llm"]
            self.base_url = self.llm["base_url"].rstrip("/")

settings = Settings()