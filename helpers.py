import os
import base64
import hashlib
import requests
from flask import session
import secrets

# Spotify API information
CLIENT_ID = os.environ["CLIENT_ID"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
SCOPES = "user-top-read"  # Add other scopes as needed

def generate_code_verifier_and_challenge():
    # Generate a code verifier and code challenge for PKCE
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=")
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier).digest()).rstrip(b"=")
    return code_verifier.decode("utf-8"), code_challenge.decode("utf-8")

code_verifier, code_challenge = generate_code_verifier_and_challenge()

# Functions

# Exchange the code for a token
def exchange_code_for_token(code):
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=data)

    if response.status_code != 200:
        return f"Failed to retrieve token: {response.text}"

    tokens = response.json()
    return tokens["access_token"]

def get_top_tracks(access_token, limit, time_range):
    # Retrieve the user"s top tracks from Spotify
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()

def get_top_artists(access_token, limit, time_range):
    # Retrieve the user"s top artists from Spotify
    url = f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()

def search(access_token, search):
    # Perform a Spotify search for playlists based on a search query
    search = str(search)
    search = search.replace(" ", "+")
    url = f"https://api.spotify.com/v1/search?q={search}&type=playlist&limit=1"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()

#shorten text function
def shorten(text):
    if len(text) > 30:
        text = text[:23] + "..."
        return text
    else:
        return text


