

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
from scape import get_url, kill_chrome_processes, powercity



# Function to send message to Telegram
async def send_message_to_telegram(message):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '6911991203:AAGuVx7-e57Aniie7YvaOswF2yR7knPd9hM'
    # Replace 'YOUR_CHAT_ID' with the chat ID you want to send messages to
    chat_id = '-4045954869'
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)



def main(url):
    
    kill_chrome_processes()
    driver, wait = get_url(url)
    powercity(driver,wait)
            
    message = 'PulseX Earn Protocol\n'
    message += '--------------------\n'
    message += process_data('0x2B12...Cd6C','PLS PV Blue')
    message += process_data('0x4A87...2CFC', 'PlsX 2nd Ledger')
    
    #send data to telegram
    asyncio.run(send_message_to_telegram(message))
    
if __name__ == "__main__":
    main('https://www.earn.powercity.io/#/')
    