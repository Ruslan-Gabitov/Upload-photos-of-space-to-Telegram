import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from requests.models import Response
from urllib.parse import urlsplit
import datetime


def get_filename_extension(urls):
    url = urlsplit(urls)
    path, filename_extension = os.path.splitext(url.path)
    return filename_extension


def create_folder(name_folder):
    Path(name_folder).mkdir(parents=True, exist_ok=True)
    return name_folder


def upload_images(urls, path):
    for id, url in enumerate(urls):
        response = requests.get(url)
        response.raise_for_status()
        filename_extension = get_filename_extension(url)
        with open(f'{path}{id+1}{filename_extension}', 'wb') as file:
            file.write(response.content)


def fetch_spacex_last_launch(flight_number):
    url = 'https://api.spacexdata.com/v3/launches/'
    params = {'flight_number': flight_number}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[0]['links']['flickr_images']


def fetch_nasa_last_launch(image_namber):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': os.getenv('NASA_TOKEN'), 'count': image_namber}
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = response.json()
    links = [link['url'] for link in urls]
    return links


def fetch_nasa_epic_last_launch():
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': os.getenv('NASA_TOKEN')}
    response = requests.get(url, params=params)
    response.raise_for_status()
    links = []
    date, times = response.json()[0]['date'].split(' ')
    aDate = datetime.date.fromisoformat(date).strftime("%Y/%m/%d")
    for namedate in response.json():
        image = namedate['image']
        links.append(f'https://api.nasa.gov/EPIC/archive/natural/{aDate}/png/{image}.png?api_key={os.getenv("NASA_TOKEN")}')
    return links


if __name__ == '__main__':
    load_dotenv()
    create_folder('images_nasaepic')
    create_folder('images_spacex')
    create_folder('images_nasa')
    upload_images(urls=fetch_spacex_last_launch(flight_number=90),
               path='images_spacex/spacex_')
    upload_images(urls=fetch_nasa_last_launch(
        image_namber=30), path='images_nasa/nasa_')
    upload_images(urls=fetch_nasa_epic_last_launch(), path='images_nasaepic/epic_')
    
