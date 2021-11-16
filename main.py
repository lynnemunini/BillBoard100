import pprint
import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# import os
# CLIENT_ID = os.environ.get("CLIENT_ID")
# CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


travel = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
# To get the current year
year = travel.split('-')[0]
# print(year)
URL = f"https://www.billboard.com/charts/hot-100/{travel}"
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "lxml")
songs = soup.findAll(name="span", class_="chart-element__information__song text--truncate color--primary")
songs_uri_list = []

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="",
        client_secret="",
        show_dialog=True,
        cache_path="token.txt"
    )
)

for each in songs:
    song = each.getText()
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri_list.append(uri)
    except IndexError:
        print("Song not in Spotify. Skipped!")

user_id = sp.current_user()["id"]
# print(user_id)
user = sp.current_user()
# print(user)
# print(songs_uri_list)
playlist_name = f"{travel} Billboard 100"
# Create a playlist
playlist = sp.user_playlist_create(user_id, name=playlist_name, public=False)

# Add items to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri_list)

