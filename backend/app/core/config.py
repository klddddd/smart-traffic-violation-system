from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/traffic_violation?charset=utf8mb4"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "change-me-in-prod"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    MEDIA_STORAGE_DIR: str = "./media"
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_IMAGE_TYPES: tuple[str, ...] = ("image/jpeg", "image/png", "image/webp")


settings = Settings()
