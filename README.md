# SpotifyAPI

## Introduction

This is a basic tutorial on how to make this API work on your windows PC. You must have a Premium Spotify account to use this application.

# Steps:

-Pip install the libraries spotipy and selenium.__
-Create an application on spotify dashboard to get client id, secret and redirect url. (do not share them)__
-Add those credentials inside the data folder\spotifyConfig.json file together with email and password of your account. Change the name of this file to spotify_config.json.__
-Download Chromdriver (pay attention to the browser's version), and add it to the environment variables.__
-Run main.py. The first time it should open a google tab with a link. Copy and paste the link in the terminal and press enter. (Note, this may exit the application, so you will need to run it again. It only happens once)__
-Run the program again and it will work.__
-The first time, the program will need to create cookies, so it will take a little longer to log in.__
-Current possible inputs are: [name_of_song], [pause], [play], [quit].
