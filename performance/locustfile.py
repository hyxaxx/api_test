from locust import HttpUser, task, between


class ApiUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)

    def on_start(self):
        r = self.client.post("/login",
                             json={"username": "admin", "password": "123456"})
        self.token = r.json()["token"]

    @task(3)
    def create_order(self):
        self.client.post("/orders", json={"amount": 100},
                         headers={"Authorization": self.token})

    @task(1)
    def get_order(self):
        self.client.get("/orders/1",
                        headers={"Authorization": self.token})