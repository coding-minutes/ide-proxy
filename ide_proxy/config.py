import os


class Config:
    DEBUG = os.environ.get("DEBUG") in ["True", "true", "1", 1]
    SECRET_KEY = os.environ.get("SECRET_KEY", "abc")
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

    IDE_CORE_URL = os.environ.get("IDE_CORE_URL")
    JUDGE_PROXY_URL = os.environ.get("JUDGE_PROXY_URL")

    JWT_SECRET = os.environ.get("JWT_SECRET", "abc")
