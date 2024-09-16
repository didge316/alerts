from datetime import datetime
import time
import subprocess


def liquid():
    result = subprocess.run(['python3','liquid_cron.py'])
    return result.returncode

def earn():
    result = subprocess.run(['python3','power_city_cron.py'])
    return result.returncode

def flex():
    result = subprocess.run(['python3','flex_cron.py'])
    return result.returncode

while True:
    current_time = datetime.now()
    hrs_mins = current_time.strftime('%H:%M')

    if hrs_mins == '22:00' or hrs_mins == '06:00' or hrs_mins == '12.00' or hrs_mins == '17.00':
        #Liquid Loans
        exit_code = liquid()
        counter = 0
        if exit_code == 0:
            time.sleep(5)
        while exit_code != 0 and counter <5:
            time.sleep(120)
            exit_code = liquid()
            counter += 1

        #Earn
        exit_code = earn()
        counter = 0
        if exit_code == 0:
            time.sleep(5)
        while exit_code != 0 and counter <5:
            time.sleep(120)
            exit_code = earn()
            counter += 1

        #Earn
        exit_code = flex()
        counter = 0
        if exit_code == 0:
            time.sleep(5)
        while exit_code != 0 and counter <5:
            time.sleep(120)
            exit_code = flex()
            counter += 1
            
            
    else:
        time.sleep(30)