import requests

def get_session():
    s = requests.Session()
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
    })
    return s