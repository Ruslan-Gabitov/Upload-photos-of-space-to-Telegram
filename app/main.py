import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlsplit
import datetime
import telegram
import time
import random

def get_filename_extension(urls):
    url = urlsplit(urls)
    path, filename_extension = os.path.splitext(url.path)
    return filename_extension


def create_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def upload_images(urls, path, name_image):
    create_folder(path)
    for id, url in enumerate(urls):
        response = requests.get(url)
        response.raise_for_status()
        filename_extension = get_filename_extension(url)
        with open(f'{path}/{name_image}{id+1}{filename_extension}', 'wb') as file:
            file.write(response.content)


def fetch_spacex_last_launch(flight_number=85):
    url = 'https://api.spacexdata.com/v3/launches/'
    params = {'flight_number': flight_number}
    response = requests.get(url, params=params)
    response.raise_for_status()
    links = response.json()[0]['links']['flickr_images']
    return links


def fetch_nasa_last_launch(image_namber=30):
    NASA_TOKEN = os.getenv('NASA_TOKEN')
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': NASA_TOKEN, 'count': image_namber}
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = response.json()
    links = [link['url'] for link in urls]
    return links


def fetch_nasa_epic_last_launch():
    NASA_TOKEN = os.getenv('NASA_TOKEN')
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': NASA_TOKEN}
    response = requests.get(url, params=params)
    response.raise_for_status()
    links = []
    date, times = response.json()[0]['date'].split(' ')
    aDate = datetime.date.fromisoformat(date).strftime("%Y/%m/%d")
    for namedate in response.json():
        image = namedate['image']
        links.append(
            f'https://api.nasa.gov/EPIC/archive/natural/{aDate}/png/{image}.png?api_key={os.getenv("NASA_TOKEN")}')
    return links


def publish_images_to_channel(chat_id, path, time_sleep=86400):
    TG_TOKEN = os.getenv('TG_TOKEN')
    bot = telegram.Bot(token=TG_TOKEN)
    for img in os.listdir(path):
        bot.send_document(chat_id=chat_id, document=open(
            f'images/{img}', 'rb'), caption='')
        time.sleep(time_sleep)
        print(f'Фото {img} опубликованно!')


if __name__ == '__main__':
    load_dotenv()
    fun = {'spacex': fetch_spacex_last_launch,
            'nasa': fetch_nasa_last_launch,
            'nasa_epic': fetch_nasa_epic_last_launch
    }
    parser = argparse.ArgumentParser(description='Программа дает возможность скачть фото \
        космоса с сайтов NASA и Spacex, а так же сделать автопостинг в ваш телеграм канал')

    parser.add_argument('down', type=str, help='Выберете чьи фото скачать и укажите в качестве \
        аргумента: spacex, nasa, nasa_epic ?')
    args = parser.parse_args()

    print(args.down)

    upload_images(urls=fun[args.down](), path='images', name_image='spacex_')

    # upload_images(urls=fetch_nasa_last_launch(),
    #               name_folder='images', name_image='nasa_')

    # upload_images(urls=fetch_nasa_epic_last_launch(),
    #               name_folder='images', name_image='epic_')

    # publish_images_to_channel(time_sleep=3, path='images', chat_id='@cosmo_mo')
