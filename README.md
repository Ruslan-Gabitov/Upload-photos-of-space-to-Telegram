# Program to download photos of space to Telegram

The script allows you to download photos of space from [NASA](https://www.nasa.gov/) and [Spacex](https://www.spacex.com/) sites using their open API and automatically publish them on Telegram
### How to install
To authorize, you must obtain a TOKEN, you can obtain it from this site [Telegram](https://romua1d.ru/en/how-to-get-token-for-telegram-bot/) and [NASA](https://api.nasa.gov/). Token must be saved to `.env` file

*Note that variables must be named exactly as in the example, and tokens after the sign are equally written without spaces*
```
NASA_TOKEN=your token
TG_TOKEN=your token

```
Also in this file, you need to create two more environment variables that will allow you to set the interval between posts to Telegram, set the time in seconds and publish photos to your telegram channel
```
TIME_SLEEP=specify the time in seconds
CHAT_ID=your id
```
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
Run the file `main.py`