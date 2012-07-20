"""Adapter for businesses and related stuff."""
from game_connector import GameConnector
from utils import lazy_property


class OutOfCityException(Exception):
    """Method that can be used only in a city was called in a wilderness."""
    pass


class UnexistingBusinessException(Exception):
    """Method was called for a business that wasn't purchased
    in current city (or just doesn't exist)."""
    pass


class UnexistingCellException(Exception):
    """Method was called for a cell that wasn't purchased
    for given business in current city (or just doesn't exist)."""
    pass


class BusinessManager:
    """Manager of businesses in a city."""

    @lazy_property
    def _business_list(self):
        """Return full list of purchased businesses in a city.
        Can raise OutOfCityException."""
        page = GameConnector.get_page('business')
        if page.find(id='message', text='There are no businesses',
                     recoursive=True):
            raise OutOfCityException

        container = page.find(attrs={'class': 'tabbernav'}, recoursive=True)
        return [Business(x.find('a').string, page) for x in container('li')]

    def __len__(self):
        return len(_business_list)

    def __getitem__(self, key):
        return _business_list[key]

    def __iter__(self):
        for business in _business_list:
            yield business

    def __reversed__(self):
        for business in reverse(_business_list):
            yield business

    #def __contains__(self, item):
        #return item in _business_list

    def __str__(self):
        return _business_list


class Business:
    def __init__(self, name, page):
        """Save name of business and the business page to be parsed later."""
        self.name = name
        self.page = page

    @lazy_property
    def _cell_list(self):
        pass

    def __len__(self):
        return len(_cell_list)

    def __getitem__(self, key):
        return _cell_list[key]

    def __iter__(self):
        for cell in _cell_list:
            yield cell

    def __reversed__(self):
        for cell in reverse(_cell_list):
            yield cell

    #def __contains__(self, item):
        #return item in _cell_list

    def __str__(self):
        return _cell_list


class Cell:
    """Business cell."""

    @property
    def status(self):
        """Return status of given cell of given business.
        Possible statuses: (not purchased/free for use/in progress/
        ready for sale)."""
        pass

    @property
    def last_process(self):
        """Return dict of last process info."""
        pass

    def release(self):
        """Sell or release in another way result of finished process."""
        pass

    def execute(self, process):
        """Start process by name."""
        pass
