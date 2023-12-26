import requests
import base64

class SpotifyClient:
    """
    A class to handle interactions with the Spotify API.
    """

    def __init__(self):
        """
        Initializes the SpotifyClient with client credentials.

        Parameters:
        - client_id: Your Spotify Application's Client ID
        - client_secret: Your Spotify Application's Client Secret
        """
        self.client_id = '83da75dc39ac4c8b96e443125017d98a'
        self.client_secret = '1c8ec73a1411435fb4bb8db67270c068'
        self.auth_url = "https://accounts.spotify.com/api/token"
        self.access_token = None
        self.headers = None

    def authenticate(self):
        """
        Authenticate with Spotify and set the access token.

        Returns:
        - True if authentication is successful
        - False if authentication fails
        """
        # Encode the Client ID and Client Secret
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        # Request headers for authentication
        auth_headers = {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

        # Request body
        data = {
            "grant_type": "client_credentials"
        }

        # POST request to get the access token
        response = requests.post(self.auth_url, headers=auth_headers, data=data)

        # If successful, set the access token and return True
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            return True
        else:
            # If there's an error, return False
            return False

    def release_date(self, song_title, artist):
        """
        Get the release date of a song.

        Parameters:
        - song_title: The title of the song
        - artist: The artist of the song

        Returns:
        - The release date of the song
        - None if the song is not found
        """
        # Search for the song
        search_url = "https://api.spotify.com/v1/search"
        search_params = {
            "q": f"track:{song_title} artist:{artist}",
            "type": "track",
            "market": "US",
            "limit": 5,
            "offset": 0
        }
        response = requests.get(search_url, headers=self.headers, params=search_params)

        # If the song is found, get the release date
        if response.status_code == 200:
            try:
                items = response.json()['tracks']['items']
                for item in items:
                    album_type = item['album']['album_type']
                    if album_type == 'album':
                        release_date = item['album']['release_date']
                        precision = item['album']['release_date_precision']
                        album = item['album']['name']
                        return album, album_type, release_date, precision
                return None
            except:
                return None
        else:
            # If the song is not found, return None
            return None

spotify_client = SpotifyClient()
spotify_client.authenticate()
print(spotify_client.release_date("Don't Start Now", "Dua Lipa"))
print(spotify_client.release_date("Levitating", "Dua Lipa"))
print(spotify_client.release_date("Levitating", "Dua Lipa feat. DaBaby"))
print(spotify_client.release_date("Break My Heart", "Dua Lipa"))
