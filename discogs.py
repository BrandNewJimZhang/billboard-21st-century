import discogs_client
import requests
from itertools import islice
from tqdm import tqdm
from datetime import datetime

class DiscogQuerier:
    def __init__(self, user_token):
        self.client = discogs_client.Client('JimZhangDiscogs/1.0', user_token=user_token)

    def find_earliest_release(self, query, artist_name=None, search_type='release', max_results=15):
        results = self.client.search(f'{artist_name} - {query}', type=search_type)

        earliest_release = None
        title = artist = released = None

        for result in tqdm(islice(results, max_results)):
            release = self.client.release(result.id)
            resp = requests.get(release.data['resource_url'], headers={'User-Agent': 'JimZhangDiscogs/1.0'})
            try:
                release_data = resp.json()
                release_date_str = release_data['released'].strip()
                release_artists = ', '.join([artist['name'] for artist in release_data['artists']])

                if artist_name and artist_name.lower() not in release_artists.lower():
                    continue

                if release_date_str:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d")

                    if earliest_release is None or release_date < earliest_release:
                        earliest_release = release_date
                        title = release_data['title']
                        artist = release_artists
                        released = release_date_str

            except (KeyError, ValueError) as e:
                # Debugging print
                print(f"Error processing release: {e}")

        return {
            "title": title,
            "artist": artist,
            "released": released
        }

# Example usage
user_token = '<your user token here>'

if __name__ == '__main__':
    querier = DiscogQuerier(user_token)
    details = querier.find_earliest_release("Beautiful Girls", "Sean Kingston")
    print(details)
