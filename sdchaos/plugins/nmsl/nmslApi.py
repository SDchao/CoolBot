import requests
from .config import API_URI

def get_new_line():
    r = requests.get(API_URI)
    if r.status_code == 200:
        return r.text
    else:
        return None