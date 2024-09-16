

from selenium import webdriver #default requirement
from selenium.webdriver.common.by import By # this is used to find elements on the page to interact with
from selenium.webdriver.chrome.options import Options #for adding options such as headless
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time, sys, re, os
import psutil
import asyncio
from telegram import Bot
from data import process_data
from scape import get_url, kill_chrome_processes, liquid



# Function to send message to Telegram
async def send_message_to_telegram(message):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '6911991203:AAGuVx7-e57Aniie7YvaOswF2yR7knPd9hM'
    # Replace 'YOUR_CHAT_ID' with the chat ID you want to send messages to
    chat_id = '-4045954869'
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)



def main(url,log_file):
    try:
        #Delete old log file
        if os.path.exists(log_file):
            os.remove(log_file)
        kill_chrome_processes()
        driver, wait = get_url(url)
        liquid(driver,wait,'0x121C...5a33',log_file)
                
        message = 'Liquid Loans\n'
        message += '--------------------\n'
        message += process_data(log_file,'0x121C...5a33','Orange Pls Withdrawals')
        
        
        #send data to telegram
        asyncio.run(send_message_to_telegram(message))

        return 0
    
    except Exception as e:
        return 1
    
if __name__ == "__main__":
    exit_code = main('https://go.liquidloans.io/#/liquidations','ll_data_log.txt')
    
    exit(exit_code)
    