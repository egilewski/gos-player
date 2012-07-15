"""Communication with GoS server."""
import urllib.request
import urllib.parse
import http.cookiejar
import settings


class AuthentificationError(Exception):
    pass


class GameConnector(object):
    """Adapter for game web-interface."""
    def __init__(self):
        """Get connector ready for use."""
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
                #urllib.request.HTTPRedirectHandler(),
                #urllib.request.HTTPHandler(debuglevel=0),
                #urllib.request.HTTPSHandler(debuglevel=0),
                urllib.request.HTTPCookieProcessor(self.cj))

        self._authentificate();

    def _get_url(self, page_name):
        """Return URL by internal page name."""
        return settings.BASEURL + settings.URLS[page_name]

    def _authentificate(self):
        """Authentificate itself to the server."""
        auth_data = {'mode': 0, 'submit': 'Enter World'}
        auth_data.update(settings.AUTH_DATA)
        page = self.get_page('login', auth_data)
        if 'Access Denied' in page:
            raise AuthentificationError('Game server replied "Access Denied"' \
                    'Check you credentials in settings.py')

    def get_page(self, page_name, data=None):
        """Return page by internal name."""
        url = self._get_url(page_name)
        data = urllib.parse.urlencode(data).encode()
        headers = {
                'Accept-Encoding': 'gzip',
                'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.2) ' \
                              'Gecko/20100101 Firefox/10.0.2 Iceweasel/10.0.2',
                }
        request = urllib.request.Request(url, data, headers)
        response = self.opener.open(request)
        return response.read().decode()

    def send_data(self, page_name, data):
        """Send data to page by it's internal name. Return page."""
        return self.get_page(page_name=page_name, data=data)
