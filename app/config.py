from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "PA-ECOZERO Multi-HubSpot API"
    version: str = "1.0.0"
    sync_interval_minutes: int = int(os.getenv("SYNC_INTERVAL_MINUTES", "15"))


settings = Settings()
