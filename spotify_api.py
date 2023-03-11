import credentials
import tasks

class Spotify:
    def __init__(self):
        #Create browser using chromedriver
        self.webBrowser=tasks.web_browser()
        
        #Create Spotipy object to use Spotipy API
        self.spotipy_object=tasks.spotipy_object(credentials.client_id, credentials.client_secret, credentials.redirect_uri)

        #Log in to Spotify Web Player
        tasks.login(self.webBrowser, credentials.email, credentials.password)
        
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

