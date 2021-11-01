import telegram
from dotenv import load_dotenv
import os
import time

def publish_images_to_channel(chat_id, time_sleep=86400):
    bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
    count = 0
    print(len(os.listdir('images')))
    for img in os.listdir('images'):
        bot.send_document(chat_id=chat_id, document=open(f'images/{img}', 'rb'), caption='')
        time.sleep(time_sleep)
        print(f'Фото {img} опубликованно!')
        count += 1
    print(count)


if __name__ == '__main__':
    load_dotenv()
    publish_images_to_channel(time_sleep=3, chat_id='@cosmo_mo')
    