from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Knowledge Graph API")
  PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
  API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
  DEBUG: bool = os.getenv("DEBUG", False)

  DB_ENDPOINT: str = os.getenv("DB_ENDPOINT", "http://localhost:7200/repositories/food-recipes")
  WIKIDATA_ENDPOINT: str = os.getenv("WIKIDATA_ENDPOINT", "https://query.wikidata.org/sparql")

  class Config:
    case_sensitive = True
    env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
  return Settings()

settings = get_settings()