import requests

class SongRecommender:
    def __init__(self, access_token):
        self.access_token = access_token
        self.genres = ['pop', 'rock', 'jazz', 'classical', 'hip-hop', 'country', 'electronic', 'folk', 'blues', 'reggae']
        self.recommended_songs = {genre: [] for genre in self.genres}
        self.liked_songs = {genre: [] for genre in self.genres}
        self.disliked_songs = {genre: [] for genre in self.genres}

    def get_next_recommendation(self):
        import random
        genre = random.choice(self.genres)
        # Fetch a song recommendation from Spotify
        url = 'https://api.spotify.com/v1/recommendations'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'seed_genres': genre,
            'limit': 1
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data['tracks']:
            track = data['tracks'][0]
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'url': track['external_urls']['spotify']
            }
        else:
            return None

    def update_preferences(self, genre, liked):
        if liked:
            self.liked_songs[genre].append(self.get_next_recommendation())
        else:
            self.disliked_songs[genre].append(self.get_next_recommendation())
