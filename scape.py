from selenium import webdriver #default requirement
from selenium.webdriver.common.by import By # this is used to find elements on the page to interact with
from selenium.webdriver.chrome.options import Options #for adding options such as headless
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import os
import psutil
import time

def get_url(url):
    # Change script to execute from cwd
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

    #Chrome stuff
    current_directory = os.getcwd()
    chrome_path =(f'{current_directory}/web/chrome-linux64/chrome')
    chromedriver_path = (f'{current_directory}/web/chromedriver')
    service = Service(executable_path=chromedriver_path)
    chrome_options = Options()
    chrome_user_data_dir = (f'{current_directory}/web/')
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
    chrome_options.add_extension(f"{current_directory}/web/meta.crx")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver,60)
    
    #login to metamask
    meta_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html'
    driver.get(meta_url)
    enter_pass = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]')))
    enter_pass.send_keys('skunkskunk')
    enter_pass.send_keys(Keys.ENTER)

    #go to main url
    driver.get(url)
    return driver, wait


    #close all chrome windows if open
def kill_chrome_processes():
    for proc in psutil.process_iter():
        try:
            # Check if the process name contains 'chrome'
            if 'chrome' in proc.name().lower():
                proc.kill()  # Terminate the process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Handle exceptions if process cannot be terminated

def powercity(driver, wait):
    # # Delete old log file
    if os.path.exists('data_log.txt'):
    # Delete the file
        os.remove('data_log.txt')
    #click risky vaults
    #driver, wait = get_url()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[1]/div[1]/nav/div[2]/a[2]'))).click()

    # get current price
    pxdc_price_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/div[3]/span[1]')))
    current_pxdc_price = pxdc_price_element.text

    while True:
        # While loop keeps clicking the next page until address is found
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/div/table')))
        time.sleep(1)
        rows = table_element.find_elements(By.TAG_NAME, "tr")

        with open('data_log.txt', 'a') as file:
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_text = '|'.join(cell.text for cell in cells)
                file.write(row_text+'\n')
        # for row in rows:
        #     # Get all cells of the row
        #     cells = row.find_elements(By.TAG_NAME, "td")
        #     for row in cells:
        #         with open('data_log.txt', 'a') as file:
        #                 file.write(row.text)

    

        # Click next page
        
        button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/h2/div/button[2]')
        if button.is_displayed() and button.is_enabled():
            button.click()
            #time.sleep(1)
        else:
            
            time.sleep(2)
            break
    driver.quit()
           
            