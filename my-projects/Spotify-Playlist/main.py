import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
# API KEYS

spotify_client = os.getenv("client_ID")
spotify_secret = os.getenv("client_SECRET")

spotify_redirect_URL = "http://example.com"

# Authorization with SPOTIPY 

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri= spotify_redirect_URL,
        client_id= spotify_client,
        client_secret= spotify_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)

# Try Catch for inputting correct TimeStamp
# Test with 2000-08-12

while True:
    try:
        TravelYear = input("What year would you like to travel to? Enter in format YYYY-MM-DD:")

        valid_date = datetime.strptime(TravelYear, "%Y-%m-%d")
        break
    except ValueError:
        print("invalid format, please try again in YYYY-MM-DD format.")

# Make a request to billboard.com

url = f"https://www.billboard.com/charts/hot-100/"+TravelYear
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
response = requests.get(url=url, headers = headers)
response.raise_for_status()

# Turn that shit into soup 

response = response.text 
soup = BeautifulSoup(response, "html.parser")

listOf100 = soup.select('li ul li h3')
songnames = [song.getText().strip() for song in listOf100]

# Search Spotify for URL's

user_id = sp.current_user(["id"])
song_urls = []
year = TravelYear.split("-")[0]

for song in songnames:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_urls.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create Playlist and load songs into it

my_playlist = sp.user_playlist_create(user=f"{user_id}", 
                                      name=f"{TravelYear} Billboard 100", 
                                      public=False,
                                      description="Top Tracks from back in the Dayz of Brunel")
sp.playlist_add_items(playlist_id=my_playlist["id"], items=song_urls)