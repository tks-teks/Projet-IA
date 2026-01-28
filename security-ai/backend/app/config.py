from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Security AI Guardian"
    database_url: str = "sqlite:///./security_ai.db"
    model_path: Path = Path("./model.joblib")
    threshold_setting_key: str = "alert_threshold"
    default_threshold: float = -0.35
    critical_threshold: float = -0.6
    auto_speech_rate_limit_sec: int = 30


settings = Settings()
