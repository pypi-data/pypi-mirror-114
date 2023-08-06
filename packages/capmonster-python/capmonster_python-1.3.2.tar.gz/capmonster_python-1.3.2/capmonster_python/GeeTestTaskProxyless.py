from .CapmonsterClient import CapmonsterClient


class GeeTestTaskProxyless(CapmonsterClient):
    def __init__(self, client_key, **kwargs):
        super().__init__(client_key=client_key, **kwargs)
        self.userAgent = kwargs.get("userAgent")
        self.solution = "solution"
        self.result_getter = "get_all"

    def createTask(self, website_url, gt, challenge):
        data = {
            "clientKey": self.client_key,
            "task":
                {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": website_url,
                    "gt": gt,
                    "challenge": challenge
                }
        }
        task = self.make_request(method="createTask", data=data)
        self.checkResponse(response=task)
        return task.json()["taskId"]
