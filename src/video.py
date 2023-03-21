import json
import os
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Video:
    """Класс для видео"""

    def __init__(self, video_id: str):
        response = self._get_info(video_id)
        self.__video_id: str = video_id  # id видео
        self.__title: str = response['items'][0]['snippet']['title']  # название видео
        self.__url: str = 'https://youtu.be/' + video_id  # ссылка на канал
        self.__view_count: int = int(response['items'][0]['statistics']['viewCount'])  # количество просмотров
        self.__like_count: int = int(response['items'][0]['statistics']['likeCount'])  # количество лайков

    def __str__(self) -> str:
        return f'{self.__title}'

    @staticmethod
    def get_service():  # возвращает объект для работы с YouTube API
        return build('youtube', 'v3', developerKey=API_KEY)

    def _get_info(self, video_id: str) -> dict:  # получает информацию о видео
        response = self.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=video_id
        ).execute()
        return response


class PLVideo(Video):
    """Класс для плейлиста"""

    def __init__(self, video_id: str, pl_id: str):
        if self._get_pl_info(pl_id, video_id):  # если видео есть в плейлисте
            super().__init__(video_id)  # вызываем конструктор Video
            self.__pl_id: str = pl_id  # создаем id плейлиста

    def _get_pl_info(self, pl_id: str, video_id: str) -> dict | None:  # получает информацию о плейлисте
        try:
            response = self.get_service().playlistItems().list(playlistId=pl_id,
                                                               part='contentDetails',
                                                               maxResults=1,
                                                               videoId=video_id
                                                               ).execute()
            return response
        except Exception as e:
            print(e)


if __name__ == '__main__':
    video = Video('9lO06Zxhu88')
    print(video)
    print(json.dumps(dict(video.__dict__.items()), indent=2, ensure_ascii=False))
    video = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    print(video)
    print(json.dumps(dict(video.__dict__.items()), indent=2, ensure_ascii=False))
    video = PLVideo('iZISBwtNGvM', 'PLA0M1Bcd0w8yWHh2V70bTtbVxJICrnJHd')
    print(video)
    print(json.dumps(dict(video.__dict__.items()), indent=2, ensure_ascii=False))
