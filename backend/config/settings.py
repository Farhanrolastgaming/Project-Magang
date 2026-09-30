import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    # Update for MySQL
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/genautopress"
    
    JWT_SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200 # 30 days
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
