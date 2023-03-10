import json
import os
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        self.channel_id = channel_id

    def get_info(self):
        response = YOUTUBE.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        return response

    def print_info(self):
        response = self.get_info()
        print(json.dumps(response, indent=2, ensure_ascii=False))
