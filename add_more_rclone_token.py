import random
import time

from msedge.selenium_tools import Edge, EdgeOptions

# import subprocess

# subprocess.Popen('start msedge.exe  --remote-debugging-port=9222 --user-data-dir="C:/EdgeTEMP" ', shell=True)
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

options = EdgeOptions()
options.use_chromium = True
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = Edge(executable_path="./msedgedriver.exe", options=options)
email_xpath = '//*[@id="identifierId"]'
password_xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
driver.get('https://accounts.google.com/')

def test():
    action = webdriver.ActionChains(driver)
    time.sleep(5)
    mail = 'mitsuekramer0058@gmail.com'
    email_elem = driver.find_element_by_xpath(email_xpath)
    action.move_to_element(email_elem).click().perform()
    email_elem.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    email_elem.send_keys(Keys.ENTER)

password = 'Fejzeddcofbm'
password_elem = driver.find_element_by_xpath(password_xpath)
for char in mail:
    time.sleep(float('0.{}'.format(random.randint(1, 3))))
    password_xpath.send_keys(char)
email_elem.send_keys(Keys.ENTER)
