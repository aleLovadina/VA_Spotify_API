import pickle
import spotipy
import cred
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from spotipy.oauth2 import SpotifyOAuth
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#spotipy object API
scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played streaming user-library-read user-read-private user-library-modify user-read-playback-position playlist-read-private playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_uri, scope=scope))

#chrome driver
webdriver_service = Service(".\chromedriver.exe")

#options
chrome_options=Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)
#option to remove error: Filed to read descriptor from node connection: A device attached to the system is not functioning
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#create browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

#open spotify on a new browser
browser.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")

#load cookies
cookies=pickle.load(open('cookies.pkl', 'rb'))

for cookie in cookies:
    cookie['domain']='.spotify.com'
    try:
        browser.add_cookie(cookie)
    except:
        pass

#open web player
browser.get('https://open.spotify.com')
browser.maximize_window()

#wait for page to load
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/nav/div[1]/ul/li[1]/a')))
    print('page ready')
except TimeoutException:
    print('loading took too much time')

#check for announcement and close it
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')))
    time.sleep(1)
    xbutton = browser.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
    xbutton.click()
except:
    pass

#end of selenium control, API takes over

#get device id
try:
    devices=sp.devices()
    dev=devices['devices']
    device_id=devices['devices'][0]['id']
    sp.transfer_playback(device_id, force_play=False)
    #print(json.dumps(devices, sort_keys=True, indent=4))
except:
    nextbtn = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
    nextbtn.click()
#song handle
query=""
while(True):

    # Search for the Song.
    query=input('What song do you want to listen to? (press x to stop) ')
    if(query=='x'):
        sp.pause_playback()
        break  
    if(query=='pause'):
        sp.pause_playback()
    elif(query=='play'):
            sp.start_playback()
    else:
        searchQuery = query
        #get results
        trackResults = sp.search(searchQuery,1,0,"track")
        trackURI=trackResults['tracks']['items'][0]['uri']
        trackSelectedList=[]
        trackSelectedList.append(trackURI)
        #sp.transfer_playback(device_id, force_play=True)
        #print(json.dumps(devices, sort_keys=True, indent=4))
        sp.start_playback(device_id, None, trackSelectedList)
    

browser.quit()
