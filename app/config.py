from pydantic_settings import SettingsConfigDict, BaseSettings


class DatabaseSetting(BaseSettings):
    POSTGRES_URL: str

    # 让它直接读取同名的环境变量（Vercel 中已设置）
    model_config = SettingsConfigDict(
        # env_prefix="",          # vercel
        env_file=".env",       # 本地
        case_sensitive=True,   # 大小写敏感
        env_ignore_empty = True,
        extra = "ignore",
    )

settings = DatabaseSetting()
print(settings)