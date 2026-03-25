from pathlib import Path

from app.core import logger

def load_prompt_file(file_name: str) -> str:
    base_dir = Path(__file__).resolve().parent.parent
    prompt_path = base_dir / "prompt" / file_name

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.critical(f"시스템 프롬프트 파일을 찾을 수 없습니다: {prompt_path}")
        raise