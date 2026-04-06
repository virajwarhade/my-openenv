import requests


class TrafficClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def reset(self, task="medium"):
        response = requests.post(
            f"{self.base_url}/reset",
            json={"task": task}
        )
        return response.json()

    def step(self, action):
        response = requests.post(
            f"{self.base_url}/step",
            json={"action": action}
        )
        return response.json()

    def state(self):
        response = requests.get(f"{self.base_url}/state")
        return response.json()