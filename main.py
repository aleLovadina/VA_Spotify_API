from spotify_api import Spotify

api=Spotify()

q=input('What song would you like to listen to? ')

while q!='quit':
    if(q=='play'):
        api.play_track()
    elif(q=='pause'):
        api.pause_track()
    else:
        api.search_track(q)
    q=input('What song would you like to listen to? ')

api.quit()
