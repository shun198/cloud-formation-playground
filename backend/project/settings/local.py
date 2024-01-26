"""LOCAL環境用の設定"""
from .base import *

DEBUG = True

REST_FRAMEWORK.update(
    {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
)

SPECTACULAR_SETTINGS = {
    "TITLE": "プロジェクト名",
    "DESCRIPTION": "詳細",
    "VERSION": "1.0.0",
}

INSTALLED_APPS += [
    "drf_spectacular",
]

ROOT_URLCONF = "project.urls.local"

# Djangoのメールの設定
EMAIL_HOST = "mail"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# SMTPの1025番ポートを指定
EMAIL_PORT = 1025
# 送信中の文章の暗号化をFalseにします
EMAIL_USE_TLS = False

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

# メールの設定
EMAIL_HOST = "mail"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_TLS = False
