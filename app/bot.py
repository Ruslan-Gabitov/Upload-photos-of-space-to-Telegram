import main
import telegram
from dotenv import load_dotenv
import os



if __name__ == '__main__':
    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
    bot.send_message(chat_id='@cosmo_mo', text='И снова привет!')
    bot.send_document(chat_id='@cosmo_mo', document=open('download.jpeg', 'rb'), caption='И снова привет!')
