import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

CLIENT_ID = os.environ("CLIENT_ID")
CLIENT_SECRET = os.environ("CLIENT_SECRET")
REDIRECT_URL = os.environ("REDIRECT_URL")
SCOPE = os.environ("SCOPE")


date_range = input("What year would you like to travel to? Type your answer in this format YYYY-MM-DD: ")
year = date_range.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_range}")
movie_website = response.text

soup = BeautifulSoup(movie_website, "html.parser")
song_category = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_list = [song.getText() for song in song_category]
print(song_list)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope=SCOPE,
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               ))

user_id = sp.current_user()["id"]

upi_list = []
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        upi_list.append(uri)
    except IndexError:
        print(f"{song} does not exist in Shopify")

print(upi_list)

create_song_playlist = sp.user_playlist_create(user=user_id, name=f"{date_range} Billboard 100", public="False")
add_songs = sp.playlist_add_items(playlist_id=create_song_playlist['id'], items=upi_list, position=None)



