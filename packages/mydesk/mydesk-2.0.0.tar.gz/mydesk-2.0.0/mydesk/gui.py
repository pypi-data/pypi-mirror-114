import time
import os.path
import platform
import subprocess
import configparser

from pathlib import Path

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from retry import retry
from gooey import Gooey, GooeyParser

@Gooey(
    program_name='MyDesk'
)
def main():
    # load/read
    default_configpath = Path.home() / "mydesk.ini"
    configpath = os.getenv("MYDESK_CONFIG_FILE", default_configpath)
    
    config = configparser.ConfigParser()
    config.read(configpath)

    parser = GooeyParser(description='MyDesk')
    parser.add_argument('website', metavar='WEBSITE', default=config['DEFAULT']['WEBSITE'])
    parser.add_argument('username', metavar='USERNAME', default=config['DEFAULT']['USERNAME'])
    parser.add_argument('password', metavar='PASSWORD', default=config['DEFAULT']['PASSWORD'], widget='PasswordField')
    parser.add_argument('secure_pin', metavar='SECURE PIN', default=config['DEFAULT']['SECURE PIN'], widget='PasswordField')
    parser.add_argument('secure_id', metavar='RSA SECURE ID')
    args = parser.parse_args()

    # change/save    
    config['DEFAULT']['WEBSITE'] = args.website
    config['DEFAULT']['USERNAME'] = args.username
    config['DEFAULT']['PASSWORD'] = args.password
    config['DEFAULT']['SECURE PIN'] = args.secure_pin

    with open(configpath, 'w') as configfile:
        config.write(configfile)

    option = Options()
    #options.add("--headless")
    
    driver = webdriver.Chrome(
                options=option, 
                executable_path="/usr/local/bin/chromedriver")
    
    try:
        driver.get(args.website)
        
        loginform_is_visible = EC.visibility_of_element_located((By.XPATH, "//form[@name='loginForm']"))
        loginform = WebDriverWait(driver, 20).until(loginform_is_visible)

        username_is_visible = EC.visibility_of_element_located((By.XPATH, "//form[@name='loginForm']//input[@name='login']"))
        username = WebDriverWait(driver, 20).until(username_is_visible)
        username.send_keys(args.username)

        password_is_visible = EC.visibility_of_element_located((By.XPATH, "//form[@name='loginForm']//input[@name='passwd']"))
        password = WebDriverWait(driver, 20).until(password_is_visible)
        password.send_keys(args.password)

        secureid_is_visible = EC.visibility_of_element_located((By.XPATH, "//form[@name='loginForm']//input[@name='passwd1']"))
        secureid = WebDriverWait(driver, 20).until(secureid_is_visible)
        secureid.send_keys(args.secure_pin + args.secure_id)
        
        loginform.submit()
        
        download_link_is_visible = EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Hosted Workstation')]"))
        download_link = WebDriverWait(driver, 20).until(download_link_is_visible)
        download_link.click()

        ica_file = waitForFile()
        
        if "macOS" in platform.platform():
            subprocess.call(["open", ica_file])
    except:
        raise
    finally:
        driver.close()

@retry(tries=5, delay=3)
def waitForFile():
    ica_file = Path(os.path.expanduser("~/Downloads/launchExtMSAD.ica"))
    if not ica_file.exists():
        raise FileNotFoundError
    return ica_file


if __name__ == '__main__':
    main()
