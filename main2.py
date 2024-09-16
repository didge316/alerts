from datetime import datetime
import time
import subprocess, os


def liquid():
    result = subprocess.run(['python3','liquid_cron.py'])
    return result.returncode

def earn():
    result = subprocess.run(['python3','power_city_cron.py'])
    return result.returncode

def flex():
    result = subprocess.run(['python3','flex_cron.py'])
    return result.returncode

# Change script to execute from cwd
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

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
    
    
    