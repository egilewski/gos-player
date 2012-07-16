"""Communication with GoS server."""
import urllib.request
import urllib.parse
import http.cookiejar
import gzip
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
        else:
            import pdb
            pdb.set_trace()

    def get_page(self, page_name, data=()):
        """Return page by internal name."""
        url = self._get_url(page_name)
        data = urllib.parse.urlencode(data).encode()
        headers = {
                'Accept-Encoding': 'gzip',
                }
        request = urllib.request.Request(url, data, headers)
        response = self.opener.open(request)
        response_headers = response.info()

        # Decompress gzip.
        if ('Content-Encoding' in response_headers.keys() and \
                    response_headers['Content-Encoding'] == 'gzip') or \
                ('content-encoding' in response_headers.keys() and \
                    response_headers['content-encoding'] == 'gzip'):
            page = gzip.GzipFile(fileobj=response)
        else:
            page = response

        return page.read().decode()

    def send_data(self, page_name, data):
        """Send data to page by it's internal name. Return page."""
        return self.get_page(page_name=page_name, data=data)
