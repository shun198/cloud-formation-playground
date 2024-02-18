from locust import HttpUser, between, task


class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def make_request(self):
        # DjangoのAPIエンドポイントに対するリクエストを実行
        response = self.client.get("/api/health")
        print(response.json())
