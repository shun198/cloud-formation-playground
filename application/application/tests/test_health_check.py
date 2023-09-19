from rest_framework import status


def test_health_check_returns_200(client):
    """ヘルスチェックで200を返すことをテスト"""
    url = "/api/health/"
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "pass"}
