import os
import base64
import hashlib
import requests
from flask import Flask, request, redirect, session, url_for, render_template
import secrets


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API information
CLIENT_ID = 'd7674a5f7c6c4621be709958d79fe2c4'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPES = 'user-top-read'  # Add other scopes as needed

# Generate a code verifier and code challenge
def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier).digest()).rstrip(b'=')
    return code_verifier.decode('utf-8'), code_challenge.decode('utf-8')

code_verifier, code_challenge = generate_code_verifier_and_challenge()


@app.route("/")
def index():
    return render_template("index.html")

# Route to start the authorization
@app.route('/login')
def login():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }
    url = f"https://accounts.spotify.com/authorize?{requests.compat.urlencode(params)}"
    return redirect(url)

# Callback route to handle the redirect from Spotify
@app.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return f"Error received from Spotify: {error}"
    if code:
        exchange_code_for_token(code)

        return redirect(url_for(session["lookup"]))

    return 'No code provided by Spotify'
"""
@app.route('/top_tracks')
def top_tracks():
    access_token = session['access_token']

    try:
        results = get_top_tracks(access_token)
        top_tracks = []
        for item in results['items']:
            track = item['name']
            artists = ', '.join([artist['name'] for artist in item['artists']])
            top_tracks.append({
                    track : artists
                    })
        return top_tracks


    except Exception as e:
        return(f"Ein Fehler ist aufgetreten: {e}")

        """

@app.route('/top_tracks', methods=['GET', 'POST'])
def top_tracks():
    if request.method == "GET":
            try:
                access_token = session['access_token']

                results = get_top_tracks(access_token)
                top_tracks = []
                track = {}
                for item in results['items']:
                    track = item['name']
                    artists = ', '.join([artist['name'] for artist in item['artists']])
                    link = item["external_urls"]["spotify"]
                    track={
                            "name": track,
                            "artist": artists,
                            "link": link,
                        }
                    top_tracks.append(track)

                return render_template('top_tracks.html', top_tracks=top_tracks)
            except  Exception as e:
                return render_template("error.html", error = e)
    else:
        session["lookup"] = "top_tracks"
        return redirect(url_for("login"))






# Exchange the code for a token
def exchange_code_for_token(code):
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier
    }
    response = requests.post('https://accounts.spotify.com/api/token', data=data)

    if response.status_code != 200:
        return f"Failed to retrieve token: {response.text}"

    tokens = response.json()
    session['access_token'] = tokens['access_token']  # Save Tokens in session
    return tokens['access_token']

def get_top_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()


