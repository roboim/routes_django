import requests
import json

from pprint import pprint


class VkGroupAdmin:
    """API VK"""
    url = "https://api.vk.com/method/"

    def __init__(self, token: str, version: str, group_id: str):
        self.token = token
        self.version = version
        self.group_id = group_id

    def post_forecast(self, forecast_str: str) -> json:
        """Опубликовать прогноз в группе"""

        url_add = "wall.post"
        params = {
            "group_id": self.group_id, "access_token": self.token, "v": self.version,
        }
        data = {
            "content": forecast_str
        }
        response = requests.post(self.url + url_add, params=params, data=data)
        pprint(response.json())
        return response.json()

    def get_users(self):
        """Получить список пользователей группы"""

        url = "groups.getMembers"
        params = {
            "group_id": self.group_id
        }
        response = requests.get(url, params=params)
        pprint(response.json())
        return response.json()
