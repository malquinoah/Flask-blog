import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

date = input('What year would you like to travel to (YYYY-MM-DD)?\n')

billboard_100_website = requests.get(url='https://www.billboard.com/charts/hot-100/' + date)

soup = BeautifulSoup(billboard_100_website.text, 'html.parser')

song_names = soup.select(selector='li ul li h3')

song_names = [song.get_text().strip() for song in song_names]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]['uri']
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)


