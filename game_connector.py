"""
Communication with GoS server.

This module is callable and holds it's state as a more convenient to use
alternative to singleton class."""
import urllib.request
import urllib.parse
import http.cookiejar
import gzip
import settings


class AuthentificationError(Exception):
    """Failer to authenticate itself to the game server."""
    pass


def get_page(page_name, data=()):
    """Return page by internal name."""
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

    return page.read().decode()


# Authentificate to the game server.
cj = http.cookiejar.CookieJar()
urlopener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
auth_data = {'mode': 0, 'submit': 'Enter World'}
auth_data.update(settings.AUTH_DATA)
page = get_page('login', auth_data)
if 'Access Denied' in page:
    raise AuthentificationError('Game server replied "Access Denied"' \
            'Check you credentials in settings.py')

