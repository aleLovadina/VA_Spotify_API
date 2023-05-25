import os
import pickle
import spotipy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from spotipy.oauth2 import SpotifyOAuth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from enum import Enum


class StatusCode(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500
    PLAY = 100
    PAUSE = 101
    STOP = 102

#Creation of browser using chromedriver
def web_browser(): 
    #webdriver_service = Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    webdriver_service = Service(os.getenv('Chromedriver'))
    
    #chromedriver options
    chrome_options=Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("detach", True)
    
    #option to remove error: Failed to read descriptor from node connection: A device attached to the system is not functioning
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])

    #create browser
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    return browser

#Creation of headless browser to create cookies
def headless_browser():
    webdriver_service = Service(os.getenv('Chromedriver'))        
    
    #chromedriver options
    chrome_options=Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")
    
    #option to remove error: Filed to read descriptor from node connection: A device attached to the system is not functioning
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #create browser
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    return browser
        
def login(browser, email, password):
    #open spotify on a new browser
    browser.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")

    #Check if cookies already exist or not
    def check_cookies():
        try: 
            with open('.\data\cookies.pkl', 'rb') as cookies:
                pickle.load(cookies)
            return StatusCode.OK.value
        except FileNotFoundError:   
            return StatusCode.NOT_FOUND.value
    
    #load cookies
    def load_cookies():
        cookies=pickle.load(open('.\data\cookies.pkl', 'rb'))
        for cookie in cookies:
            cookie['domain']='.spotify.com'
            try:
                browser.add_cookie(cookie)
            except:
                pass
    
    #if cookies already exist, open a normal browser
    if check_cookies()==StatusCode.OK.value:
        load_cookies()
    #if cookies do not exist, we need to create them
    elif check_cookies()==StatusCode.NOT_FOUND.value:
        hl_browser=headless_browser()
        
        #open spotify on a new headless browser
        hl_browser.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
       
        #wait until page is loaded
        try:
            WebDriverWait(hl_browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-button"]')))
        except TimeoutException:
            return StatusCode.SERVER_ERROR.value

        #insert email
        emailBox = hl_browser.find_element(By.XPATH, '//*[@id="login-username"]')
        
        for c in email:
            emailBox.send_keys(c)

        #insert password
        passwordBox = hl_browser.find_element(By.XPATH, '//*[@id="login-password"]')
        for c in password:
            passwordBox.send_keys(c)

        #click login button
        logbutton = hl_browser.find_element(By.XPATH, '//*[@id="login-button"]')
        logbutton.click()

        #wait for page to load 
        try:
            WebDriverWait(hl_browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[2]/div/div[1]/button')))
        except TimeoutException:
            return StatusCode.UNAUTHORIZED.value
        
        #cookies creation
        cookies=hl_browser.get_cookies()
        pickle.dump(cookies , open(".\data\cookies.pkl","wb"))

        hl_browser.quit()

        #Now we can add the cookies we just created to the browser
        load_cookies()

    #Opening web player using our account
    browser.get('https://open.spotify.com')
    browser.maximize_window()

    #wait for page to load
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/nav/div[1]/ul/li[1]/a')))
        #print('page ready')
    except TimeoutException:
        return StatusCode.SERVER_ERROR.value
    
    #clicking the home button (link) to activate the web player LU0q0itTx2613uiATSig
    (browser.find_element(By.CLASS_NAME, 'mnipjT4SLDMgwiDCEnRC')).click()
    
def spotipy_object(client_id, client_secret, redirect_uri):
    #Creation of Spotipy API object
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played streaming user-library-read user-read-private user-library-modify user-read-playback-position playlist-read-private playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    
    return sp

#Search for a song
def search_track(spotipy_object, searchQuery):
    #get id
    device_id=getDevice(spotipy_object)

    #get results
    trackResults = spotipy_object.search(searchQuery,1,0,"track")
    trackURI=trackResults['tracks']['items'][0]['uri']
    trackSelectedList=[]
    trackSelectedList.append(trackURI)
    spotipy_object.start_playback(device_id, None, trackSelectedList)
    
    return StatusCode.ACCEPTED.value

#Gets a device id
def getDevice(spotipy_object):
    #get device id
    devices=spotipy_object.devices()
    device_id=devices['devices'][0]['id']
    #not needed to transfer playback from one device to another. in case of bugs, try adding it
    #self._sp.transfer_playback(device_id, force_play=False)
    return device_id

#Play track
def play_track(spotipy_object):
    spotipy_object.start_playback()
    return StatusCode.PLAY.value

#Pause track
def pause_track(spotipy_object):
    spotipy_object.pause_playback()
    return StatusCode.PAUSE.value

#Stop application
def quit(browser, spotipy_object):
    try:
        spotipy_object.pause_playback()
    except:
        pass
    browser.quit()
    return StatusCode.STOP.value

#----other functions----
