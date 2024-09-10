

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


# Change script to execute from cwd
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)
current_directory = os.getcwd()

# Delete old log file
if os.path.exists('data_log.txt'):
    # Delete the file
    os.remove('data_log.txt')

# Function to send message to Telegram
async def send_message_to_telegram(message):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '6911991203:AAGuVx7-e57Aniie7YvaOswF2yR7knPd9hM'
    # Replace 'YOUR_CHAT_ID' with the chat ID you want to send messages to
    chat_id = '-4045954869'
    
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

chrome_path ='web/chrome-linux64/chrome'
chromedriver_path = 'web/'
# Set up the service
service = Service(executable_path=chromedriver_path)


#Chrome stuff
chrome_options = Options()
chrome_user_data_dir = (f'{current_directory}/web/')
chrome_options.binary_location = chrome_path
chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
chrome_options.add_extension(f"{current_directory}/web/meta.crx")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver,60)
my_address ='0x4A87...2CFC' # metamask main
#my_address ='0x2B12...Cd6C' #PLS PV Blue

#close all chrome windows if open
def kill_chrome_processes():
    for proc in psutil.process_iter():
        try:
            # Check if the process name contains 'chrome'
            if 'chrome' in proc.name().lower():
                proc.kill()  # Terminate the process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Handle exceptions if process cannot be terminated

# Call the function to kill all Chrome processes




#login to metamask
def meta_login():
    meta_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html'
    driver.get(meta_url)
    enter_pass = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]')))
    enter_pass.send_keys('skunkskunk')
    enter_pass.send_keys(Keys.ENTER)




#scrape data from powercity
def power_city():
    url = 'https://www.earn.powercity.io/#/'
    driver.get(url)

    #click risky vaults
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[1]/div[1]/nav/div[2]/a[2]'))).click()

    # get current price
    pxdc_price_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/div[3]/span[1]')))
    current_pxdc_price = pxdc_price_element.text

    while True:
        # While loop keeps clicking the next page until address is found
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/div/table')))
        time.sleep(1)
        rows = table_element.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            # Get all cells of the row
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                address = cells[0].text
                if address != my_address:
                    # Extract data and write to log file
                    loan_data = f"{address}|{cells[1].text}|{cells[2].text}|{cells[3].text}\n"
                    with open('data_log.txt', 'a') as file:
                        file.write(loan_data)
                else:
                    #print('My address found')
                    break  # Exit the for loop if my address is found

        # Check if my address was found and break the while loop
        if address == my_address:
            my_collaterol = cells[3].text
            break

        # Click next page
        button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/h2/div/button[2]')
        button.click()
        time.sleep(1)
        
    # Quit the driver after processing
    driver.quit()
    return(current_pxdc_price,my_collaterol)


def data():
    # Process data
    with open('data_log.txt','r') as file:
        data = file.readlines()

    total_pxdc = 0
    total_vaults = 0
    for line in data:
        line = line.strip()
        total_vaults +=1
        components = line.split('|')
        pxdc = components[2]
        pxdc = pxdc.replace(',','')

        if 'K' in pxdc:
        # Convert shorthand notation 'K' to 1000
            pxdc = float(pxdc.replace('K', '')) * 1000
        elif 'M' in pxdc:
        # Convert shorthand notation 'M' to 1000000
            pxdc = float(pxdc.replace('M', '')) * 1000000
        else:
        # If no shorthand notation, try to convert directly
            pxdc = float(pxdc)

        pxdc = float(pxdc)
        total_pxdc += pxdc
        
    #format into commas and remove decimal
    formatted_pxdc = "{:,.0f}".format(total_pxdc)
    return(total_vaults,formatted_pxdc)


def main():
    #functions to run the program
    counter = 0
    
    time.sleep(5)
    while counter <= 1:
        try:
                     
            meta_login()
            current_pxdc_price,my_collaterol = power_city()
            break
        except Exception as e:
            counter += 1
            #asyncio.run(send_message_to_telegram(f'Power city failed, waiting 1 minute for retry'))
            driver.quit()
            time.sleep(300)

    total_vaults,formatted_pxdc = data()
    #send data to telegram
    asyncio.run(send_message_to_telegram(f'------PowerCity-MM----\n{total_vaults} Vaults Below\n${formatted_pxdc} Buffer\n$1 = {current_pxdc_price}\n{my_collaterol} Collaterol in Vault\n----------------------------------'))
    driver.quit()
if __name__ == "__main__":
    main()
    