import requests
from datetime import datetime
import json
import config

class VKBackupPhoto:
    """
    Класс для работы с API VK, который принимает три аргумента: access_token, user_id, yandex_token.
    """
    def __init__(self, access_token, user_id, yandex_token, version='5.131'):
        self.vk_token = access_token
        # access_token = config.VK_ACCESS_TOKEN
        self.id = user_id
        self.yandex_token = yandex_token
        self.version = version
        self.vk_params = {'access_token': config.VK_ACCESS_TOKEN, 'v': self.version}
        self.headers = {'Authorization': f'OAuth {self.yandex_token}'}


    def get_photos(self, album_id='profile', count=5):
        """
        Метод получает фотографии (5 по умолчанию) из альбома пользователя из его профиля (по умолчанию - аватарок).
        Если нужно получить фотографии из других альбомов, то в аргументе album_id нужно передать:
        wall — фотографии со стены;
        saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        Если нужно сохранить другое количество фотографий, то нужно передать другой аргумент count (например, count=10).
        """
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': album_id,
            'extended': 1,
            'count': count
        }
        response = requests.get(url, params={**self.vk_params, **params})
        response_data = response.json()
        if 'response' in response_data:
            return response_data['response']['items']
        else:
            print("Ошибка в ответе:", response_data)
            return []  # Возвращаем пустой список в случае ошибки


    def analyze_likes(self, photos):
        """
        Данный метод анализирует кол-во лайков у каждой фотографии.
        Так как мы называем фотографию количеством ее лайков, то мы считаем количество лайков для каждой фотографии
        """
        like_counts = {}
        for photo in photos:
            likes = photo['likes']['count']
            if likes in like_counts:
                like_counts[likes] += 1
            else:
                like_counts[likes] = 1
        return {k for k, v in like_counts.items() if v > 1}


    def check_folder_exists(self, folder_path):
        """
        Данный метод проверяет существование папки для сохранения фотографий на Яндекс.Диске.
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': folder_path}
        response = requests.get(url, headers=self.headers, params=params)
        return response.status_code != 404


    def create_folder(self, folder_path):
        """
        Данный метод создает папку на Яндекс.Диске.
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': folder_path}
        requests.put(url, headers=self.headers, params=params)


    def upload_file(self):
        """
        Данный метод загружает фотографии на Яндекс.Диск в папку Saved Images.
        """
        if not self.check_folder_exists('Saved Images'):
            self.create_folder('Saved Images')

        photos = self.get_photos()
        repeated_likes = self.analyze_likes(photos)
        uploaded_files = []

        response = None

        for photo in photos:
            likes_count = photo['likes']['count']
            upload_date = datetime.fromtimestamp(photo['date']).strftime('%Y-%m-%d')
            file_name = f'{likes_count}_{upload_date}.jpg' if likes_count in repeated_likes else f'{likes_count}.jpg' #Имя файла в зависимости от количества лайков

            if not self.file_exists_on_disk(file_name):
                url_ = photo['sizes'][-1]['url']
                url_for_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                params = {'path': f'Saved Images/{file_name}', 'url': url_}
                response = requests.post(url_for_upload, params=params, headers=self.headers)
                if response.status_code == 202:
                    print(f'Файл {file_name} успешно загружен на Яндекс.Диск')
                    file_size = 'z' #Тут можно добавить получение другого разрешения фото (по умолчанию z - максимальное)
                    uploaded_files.append({"file_name": file_name, "size": file_size})
                else:
                    print('Что-то пошло не так. Файл не загружен на Яндекс.Диск')
            else:
                print(f'Файл {file_name} уже существует на диске')

        # Обновляем JSON-файл с информацией о загруженных файлах. Если в файле уже есть данные, то обновляем их
        if uploaded_files:
            print('Загруженные файлы в JSON:', uploaded_files)
            with open('uploaded_photos_info.json', 'w') as f:
                json.dump(uploaded_files, f, indent=4)
        else:
            print('Нет файлов для загрузки. JSON-файл не обновлен')

        return uploaded_files


    def file_exists_on_disk(self, file_path):
        """
        Метод, который дает информацию о существовании файла в папке на Яндекс.Диск
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'Saved Images/{file_path}'}
        response = requests.get(url, headers=self.headers, params=params)
        return response.status_code != 404


print('Привет! Я помогу тебе сохранить фотографии на Яндекс.Диск!\n'
      'Мы создадим отдельную папку Saved Images на твоем Яндекс.Диск и загрузим фотографии с твоего профиля.\n'
      'Для этого мне понадобится кое-что от тебя:\n')
yandex_token = str(input('Введи свой Яндекс токен и нажми Enter: '))
vk_id = int(input('Введи свой VK ID: '))

if yandex_token == '' or vk_id == '':
    print('Нужно ввести корректные Яндекс токен и VK ID. Попробуй еще раз')
else:
    vk = VKBackupPhoto(config.VK_ACCESS_TOKEN, vk_id, yandex_token)
    vk.create_folder('Saved Images')
    vk.upload_file()



