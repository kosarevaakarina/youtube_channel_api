import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Youtube:
    def __init__(self, channel_id):
        self.__channel_id = channel_id

        """Получение данных о ютуб-канале по его ID и ключу"""
        load_dotenv()
        api_key: str = os.getenv('YT_API_KEY')  # получение ключа из файла .env
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        """Инициализация атрибутов класса"""
        # название канала
        self.title = self.channel['items'][0]['snippet']['title']
        # описание канала
        self.description = self.channel['items'][0]['snippet']['description']
        # ссылка на канал
        self.url = 'https://www.youtube.com/' + self.__channel_id
        # количество подписчиков
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        # количество видео
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        # общее количество просмотров
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self) -> str:
        """Получение id канала"""
        return self.__channel_id

    def to_json(self, name_json):
        """Сохраняет информацию по каналу, хранящуюся в атрибутах экземпляра класса в json-файл"""
        with open(name_json, 'w', encoding='UTF=8') as file:
            data = {
                'id': self.__channel_id, 'title': self.title, 'description': self.description, 'url': self.url,
                'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                'view_count': self.view_count
            }
            return json.dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def get_service() -> object:
        """Возвращает объект для работы с API ютуба"""
        load_dotenv()
        api_key: str = os.getenv('YT_API_KEY')  # получение ключа из файла .env
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self):
        """Вывод инфорации о ютуб-канале в консоль"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def __str__(self) -> str:
        """Возвращает информацию о канале (название канала)"""
        return f'Youtube-канал: {self.title}'

    def __gt__(self, other) -> bool:
        """Сравнивает количество подписчиков"""
        if isinstance(other, Youtube):
            return int(self.subscriber_count) > int(other.subscriber_count)

    def __add__(self, other) -> int:
        """Суммирует количество подписчиков"""
        if isinstance(other, Youtube):
            return int(self.subscriber_count) + int(other.subscriber_count)
