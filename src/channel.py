import json
import os
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        self.__channel_id: str = channel_id  # id канала
        response = self.get_info()
        self.__title: str = response['items'][0]['snippet']['title']  # название канала
        self.__description: str = response['items'][0]['snippet']['description']  # описание канала
        self.__url: str = 'https://www.youtube.com/channel/' + channel_id  # ссылка на канал
        self.__subscribers: int = response['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.__video_count: int = response['items'][0]['statistics']['videoCount']  # количество видео
        self.__view_count: int = response['items'][0]['statistics']['viewCount']  # общее количество просмотров

    @classmethod
    def get_service(cls):  # возвращает объект для работы с YouTube API
        return build('youtube', 'v3', developerKey=API_KEY)

    def to_json(self, filename: str) -> None:  # сохраняет в файл значения атрибутов экземпляра Channel
        data = dict(map(lambda i: (i[0].removeprefix('_Channel__'), i[1]), self.__dict__.items()))
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_info(self) -> dict:  # получает информацию о канале
        response = self.get_service().channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        return response

    def print_info(self):  # выводит на экран информацию о канале
        response = self.get_info()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    # геттеры для атрибутов экземпляров
    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscribers(self):
        return self.__subscribers

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count
