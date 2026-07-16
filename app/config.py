import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://taskflow:taskflow@localhost:5432/taskflow",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
