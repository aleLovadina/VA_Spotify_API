import tasks
import os
import utils

class Spotify:
    def __init__(self):
        #Create browser using chromedriver
        self.webBrowser=tasks.web_browser()
        
        #Create Spotipy object to use Spotipy API
        self.data_path = os.path.join(os.getcwd(),'data', 'spotify_config.json')
        self.config_data = utils.get_json_variables(self.data_path, ['client_id', 'client_secret', 'redirect_uri', 'email', 'password'])

        self.spotipy_object=tasks.spotipy_object(self.config_data['client_id'], self.config_data['client_secret'], self.config_data['redirect_uri'])

        #Log in to Spotify Web Player
        tasks.login(self.webBrowser, self.config_data['email'], self.config_data['password'])
        
    #Search for a song and play it
    def search_track(self, query):
        tasks.search_track(self.spotipy_object, query)

    #Resume playback of a track
    def play_track(self):
        tasks.play_track(self.spotipy_object)

    #Pause playback
    def pause_track(self):
        tasks.pause_track(self.spotipy_object)

    #-----Define other useful functions-----

    #Stop playback and quit browser
    def quit(self):
        tasks.quit(self.webBrowser, self.spotipy_object)

