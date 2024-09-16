from selenium import webdriver #default requirement
from selenium.webdriver.common.by import By # this is used to find elements on the page to interact with
from selenium.webdriver.chrome.options import Options #for adding options such as headless
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
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

def powercity(driver, wait,log_file):
       
    #click risky vaults, refresh 5 times if not loading
    # count = 0
    # while count < 5:
    #     try:
    #         wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[1]/div[1]/nav/div[2]/a[2]'))).click()
    #     except:
    #         driver.refresh()
    #         count += 1
    #         time.sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[1]/div[1]/nav/div[2]/a[2]'))).click()
    # get current price
    #pxdc_price_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/div[3]/span[1]')))
    #current_pxdc_price = pxdc_price_element.text

    while True:
        # While loop keeps clicking the next page until address is found
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/div/table')))
        time.sleep(1)
        rows = table_element.find_elements(By.TAG_NAME, "tr")

        with open(log_file, 'a') as file:
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_text = '|'.join(cell.text for cell in cells)
                file.write(row_text+'\n')
        
        # Click next page
        button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/h2/div/button[2]')
        if button.is_displayed() and button.is_enabled():
            button.click()
            #time.sleep(1)
        else:
            time.sleep(2)
            break
    driver.quit()
           
def liquid(driver,wait,my_address,log_file):
    
     # Get table data
     #print('deleted old log')
    while True:

        # Get table data
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="openVaults"]/div[2]/table')))
        except TimeoutException:
            driver.quit()
            driver.get('https://go.liquidloans.io')
            time.sleep(1)
            driver.get('https://go.liquidloans.io/#/liquidations')
            time.sleep(1)
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="openVaults"]/div[2]/table')))
            except TimeoutException:
                #asyncio.run(send_message_to_telegram('Liquid Loans timed out'))
                exit()
        table_element = driver.find_element(By.XPATH, '//*[@id="openVaults"]/div[2]/table')
        time.sleep(1)
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            #print(row)
            # Get all cells of the row
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 4:
                address = cells[0].text
                if address != my_address:
                    # Extract data and write to log file
                    loan_data = f"{address}|{cells[1].text}|{cells[2].text}|{cells[3].text}\n"
                    with open(log_file, 'a') as file:
                        file.write(loan_data)
                else:
                    print('My address found')
                    print(loan_data)
                    break  # Exit the loop if my address is found

        # Check if my address was found and break the loop
        if address == my_address:
            #print(address)
            my_collaterol = cells[3].text
            break

        # Click next page
        #wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="openVaults"]/div[2]/div/button[2]'))).click()
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="openVaults"]/div[2]/div/button[2]'))).click()
        #button = driver.find_element(By.XPATH, '//*[@id="openVaults"]/div[2]/div/button[2]')
        #button.click()
        #time.sleep(5)
            

    # Quit the driver after processing
    driver.quit()