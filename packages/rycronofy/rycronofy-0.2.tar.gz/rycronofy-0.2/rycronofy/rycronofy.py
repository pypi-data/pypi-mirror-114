import requests

def refresh_access_token(client_id, client_secret, refresh_token):
    """
    Uses the specified client id, client secret, and refresh token to obtain
    a new temporary access token. Returns the access token.
    """
    token = requests.post('https://api.cronofy.com/oauth/token', data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }).json()
    return token['access_token']


def get_events(from_date, to_date, access_token):
    """
    Gets all events occurring between `from_date` and `to_date`, using the
    specified access token.
    Returns a Response object with a 200 status code if successful, or a
    401 status code if the access token is invalid.
    """
    return requests.get(f'https://api.cronofy.com/v1/events?from={from_date}&to={to_date}&tzid=America%2FLos_Angeles', headers = {
        'Authorization': f'Bearer {access_token}'
    })
