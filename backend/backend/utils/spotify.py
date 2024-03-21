SPOTIFY_API_V1_URL = 'https://api.spotify.com'

def make_header(token: str):
  return { 'Authorization': f'Bearer {token}' }
