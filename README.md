## BackupPhoto - это бесплатная программа резервного копирования фотографий профиля VK в отдельную папку на Яндекс.Диск!

### Важные моменты: 
- для запуска программы нужно скачать файл **Backup.py**
- При себе нужно иметь **токен Яндекс Полигона** (для загрузки фотографий в отдельную папку 'Saved Images' на Яндекс.Диск
- Также нужно иметь при себе **id своей страницы VK**. Нам потребуется именно id, состоящий из цифр. Получить его можно следующим способом: нужно перейти на сайт https://regvk.com/ и вставить ссылку на свой профиль. Далее нужно скопировать все цифры после "id". Они нам и потребуются
- По умолчанию будут сохраняться фотографии профиля (аватарки). Также можно получить фотографии со стены. Для этого в аргументе album_id нужно передать значение 'wall'.
- Также по умолчанию эта программа совершенно бесплатно сохраняет фотографии в максимальном разрешении! 

### Дополнительно:
1. Все зависимости находятся в файле requirements.txt
2. Фотографии будут сохраняться с именами в виде цифр. Это не просто цифры, а количество лайков у сохраняемой фотографии.
3. Будет создаваться и заполняться JSON-файл с информацией о загруженных фото.

