"""
Communication with GoS server.

This module provides only one funtion get_page(), is callable and holds it's state as a more convenient to use
alternative to singleton class.
"""
import urllib.request
import urllib.parse
import http.cookiejar
import gzip
from bs4 import BeautifulSoup
import settings


class AuthentificationError(Exception):
    """Failer to authenticate itself to the game server."""
    pass


def get_page(page_name, data=()):
    """
    Return game page by internal name.

    page_name must reference a key from settings.URLS dict.
    data is a dict to be sended via POST.
    Return value is a BeautifulSoup4 object with a page.
    """
    url = settings.BASEURL + settings.URLS[page_name]
    data = urllib.parse.urlencode(data).encode()
    headers = {'Accept-Encoding': 'gzip'}
    request = urllib.request.Request(url, data, headers)
    response = urlopener.open(request)
    response_headers = response.info()

    if (response_headers.get('Content-Encoding', None) == 'gzip'):
        page = gzip.GzipFile(fileobj=response)
    else:
        page = response

    page_content = page.read().decode()
    soup = BeautifulSoup(page_content)
    return soup


# Authentificate to the game server.
cj = http.cookiejar.CookieJar()
urlopener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
auth_data = {'mode': 0, 'submit': 'Enter World'}
auth_data.update(settings.AUTH_DATA)
page = get_page('login', auth_data)
if 'Access Denied' in page:
    raise AuthentificationError('Game server replied "Access Denied"' \
                                'Check you credentials in settings.py')
