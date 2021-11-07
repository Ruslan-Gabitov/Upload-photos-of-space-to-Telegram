import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlsplit
from urllib.parse import unquote
import datetime
import telegram
import time


def get_file_extension(urls):
    path, filename_extension = os.path.split(urlsplit(urls).path)
    filename, extension = os.path.splitext(filename_extension)
    return unquote(filename), extension



def upload_images(urls, path):
    Path(path).mkdir(parents=True, exist_ok=True)
    for ids, url in enumerate(urls):
        response = requests.get(url)
        response.raise_for_status()
        filename, extension = get_file_extension(url)
        with open(f'{path}/{filename}{ids+1}{extension}', 'wb') as file:
            file.write(response.content)


def fetch_spacex_last_launch(flight_number=85):
    url = 'https://api.spacexdata.com/v3/launches/'
    params = {'flight_number': flight_number}
    response = requests.get(url, params=params)
    response.raise_for_status()
    links = response.json()[0]['links']['flickr_images']
    return links


def fetch_nasa_last_launch(token, image_namber=30):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': token, 'count': image_namber}
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = response.json()
    links = [link['url'] for link in urls]
    return links


def fetch_nasa_epic_last_launch(token, number_links=1):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    links = []
    date, times = response.json()[0]['date'].split(' ')
    aDate = datetime.date.fromisoformat(date).strftime("%Y/%m/%d")
    for namedate in response.json():
        image = namedate['image']
        links.append(
            f'https://api.nasa.gov/EPIC/archive/natural/{aDate}/png/{image}.png?api_key={token}')
        if len(links) >= number_links:
            return links


def publish_images_to_channel(token, chat_id, path, time_sleep=86400):
    bot = telegram.Bot(token=token)
    for img in os.listdir(path):
        bot.send_document(chat_id=chat_id, document=open(
            f'images/{img}', 'rb'), caption='')
        time.sleep(time_sleep)


if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    time_sleep = os.getenv('TIME_SLEEP')
    chat_id = os.getenv('CHAT_ID')

    # try:
    #     links_spacex = fetch_spacex_last_launch(flight_number=85)
    #     links_nasa = fetch_nasa_last_launch(nasa_token, image_namber=5)
    #     links_nasa_epic = fetch_nasa_epic_last_launch(nasa_token)
    # except IndexError:
    #     print('Что-то пошло не так =(, попробуй еще раз.')
    # except ConnectionError:
    #     print('Ошибка соединения с сервером, попробуй еще раз.')
    
    # full_list_links = links_spacex + links_nasa + links_nasa_epic

    # upload_images(urls=full_list_links, path='images', name_image='image_space_')
    # try:
    publish_images_to_channel(tg_token, chat_id=chat_id, path='images', time_sleep=int(time_sleep))
    # except ConnectionError:
    #     print('Ошибка соединения с сервером, попробуй еще раз.')
        publish_images_to_channel(token=tg_token, chat_id=chat_id, path='images', time_sleep=int(time_sleep))
    except ConnectionError:
        print('Ошибка соединения с сервером, попробуй еще раз.')

    

    