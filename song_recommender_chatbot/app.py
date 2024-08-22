from flask import Flask, request, redirect, url_for, jsonify, render_template, session
import requests
import base64
import song_recommender  # Import the song recommendation logic

app = Flask(__name__)

SPOTIFY_CLIENT_ID = 'a65b50198e8543399832102ff8baa930'
SPOTIFY_CLIENT_SECRET = '9c18d0a8d4b541648bb167fd5ec0e3d6'
REDIRECT_URI = 'https://laughing-sniffle-gj9w66rpvjrc5x5.github.dev/callback'  # Replace with your actual URL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user-library-read"
    )
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f"Basic {create_auth_header(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, headers=headers, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    })
    response_data = response.json()
    session['access_token'] = response_data['access_token']
    return redirect(url_for('index'))

@app.route('/recommend')
def recommend():
    recommender = song_recommender.SongRecommender(session.get('access_token'))
    recommendation = recommender.get_next_recommendation()
    return jsonify(recommendation)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    genre = data.get('genre')
    liked = data.get('liked')
    recommender = song_recommender.SongRecommender(session.get('access_token'))
    recommender.update_preferences(genre, liked)
    recommendation = recommender.get_next_recommendation()
    return jsonify(recommendation)

def create_auth_header(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
