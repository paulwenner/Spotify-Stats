import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to get top tracks
def get_top_tracks(sp, Limit):
    # Get Top Tracks
    results = sp.current_user_top_tracks(limit=Limit)  # Get the top tracks

    return results

# Function to get top artists
def get_top_artists(sp, Limit):
    # Get Top Artists
    results = sp.current_user_top_artists(limit=Limit)  # Get the top artists

    return results

# Function to find the most common genre in a list
def most_common(lst):
    # Count the frequency of each genre in the list
    genre_frequencies = {}
    for genre in lst:
        if genre in genre_frequencies:
            genre_frequencies[genre] += 1
        else:
            genre_frequencies[genre] = 1

    # Find the genre with the highest frequency
    most_common_genre = max(genre_frequencies, key=genre_frequencies.get)
    return most_common_genre

# Function to find the top three most common genres from a user's top artists
def top_genres(sp):
    r = get_top_artists(sp, 100)
    genre_list = []

    for item in r["items"]:
        genres = item["genres"]

        for genre in genres:
            genre_list.append(genre)

    # Count the frequency of each genre in the list
    genre_frequencies = {}
    for genre in genre_list:
        if genre in genre_frequencies:
            genre_frequencies[genre] += 1
        else:
            genre_frequencies[genre] = 1

    # Use the "sorted" function and a lambda function to sort genres by frequency
    sorted_genres = sorted(genre_frequencies.items(), key=lambda x: x[1], reverse=True)

    # Get the top three most common genres
    top_three_genres = [genre for genre, count in sorted_genres[:3]]
    return top_three_genres

if __name__ == "__main__":
    # Define Credentials
    client_id = "d7674a5f7c6c4621be709958d79fe2c4"
    client_secret = "a78354b8411e44ac91f2183709f48569"
    redirect_uri = "http://localhost:8888/callback"

    # Define Scopes
    scopes = 'user-top-read'

    # Spotify OAuth configuration
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scopes,
                            cache_path='.spotipy_cache')  # Save token to the system

    #Favourite Songs

    sp = spotipy.Spotify(auth_manager=sp_oauth)
    try:
        results = get_top_tracks(sp, 10)

        # Iterate through the list of top tracks
        for i, item in enumerate(results['items']):
            track = item['name']
            artists = ', '.join([artist['name'] for artist in item['artists']])
            print(f"{i+1}: {track} by {artists}")
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"There was an error with authentication: {e}")





