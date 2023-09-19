"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str = "django"
    ALLOWED_HOSTS: str = "localhost 127.0.0.1 [::1]"
    POSTGRES_NAME: str = "django"
    POSTGRES_USER: str = "django"
    POSTGRES_PASSWORD: str = "django"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    TRUSTED_ORIGINS: str = "http://localhost"


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_SES_REGION_ENDPOINT: str = "email.ap-northeast-1.amazonaws.com"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    DEFAULT_FROM_EMAIL: str = "django@example.com"
    AWS_PROFILE: str = "localstack"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
