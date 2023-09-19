import pytest
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient

from application.tests.common_method import login, mail_confirm


@pytest.mark.django_db()
class TestInviteUser:
    # 今回は該当するエンドポイントへテストを行いたいのでAPIClientを使用します
    client = APIClient()
    url = "/api/users/send_invite_user_mail/"

    def test_management_user_can_send_invite_user_email(
        self, login_management, email_data
    ):
        """管理者ユーザで正常に招待メールを送信できることをテスト"""
        login(self.client, login_management)
        response = self.client.post(self.url, email_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        mail_confirm(mail.outbox, email_data["email"], "ようこそ")

    def test_general_user_cannot_send_invite_user_email(
        self, login_general, email_data
    ):
        """一般ユーザで正常に招待メールを送信できないことをテスト"""
        login(self.client, login_general)
        response = self.client.post(self.url, email_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_part_time_user_cannot_send_invite_user_email(
        self, login_part_time, email_data
    ):
        """アルバイトユーザで招待メールを送信できないことをテスト"""
        login(self.client, login_part_time)
        response = self.client.post(self.url, email_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
