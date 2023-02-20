import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build

class Youtube:
    def __init__(self, channel_id):
        """Получение данных о ютуб-канале по его ID и ключу"""
        self.channel_id = channel_id

        load_dotenv()
        api_key: str = os.getenv('YT_API_KEY') #получение ключа из файла .env
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def print_info(self):
        """Вывод инфорации о ютуб-канале в консоль"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

