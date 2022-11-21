import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import cred


#chrome driver
webdriver_service = Service(".\chromedriver.exe")

#options
chrome_options=Options()
chrome_options.add_argument("--no-sandbox")
#option to remove error: Filed to read descriptor from node connection: A device attached to the system is not functioning
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#create browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

#open spotify on a new browser
browser.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")

#wait until page is loaded
#time.sleep(100)
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-button"]/div[1]')))
    print('page ready')
except TimeoutException:
    print('loading took too much time')

#insert email
email = browser.find_element(By.XPATH, '//*[@id="login-username"]')
for c in cred.user:
    email.send_keys(c)

#insert password
password = browser.find_element(By.XPATH, '//*[@id="login-password"]')
for c in cred.passw:
    password.send_keys(c)

#click login button
logbutton = browser.find_element(By.XPATH, '//*[@id="login-button"]/div[1]')
logbutton.click()



time.sleep(10)
#cookies
cookies=browser.get_cookies()
print(cookies)
pickle.dump(cookies , open("cookies.pkl","wb"))


browser.quit()