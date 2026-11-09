#A5
import requests
from arsenal.comun import TIMEOUT

sesiune = requests.Session()

def cere(url, **kw):
    return sesiune.get(url, timeout=TIMEOUT, **kw)

def exista(url):
    return cere(url).status_code == 200