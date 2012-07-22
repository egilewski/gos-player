"""Adapter for businesses and related stuff."""
from game_connector import get_page
from utils import lazy_property


class OutOfCityException(Exception):
    """Method that can be used only in a city was called in a wilderness."""
    pass


class UnexistingBusinessException(Exception):
    """
    Method was called for a business that wasn't purchased in current
    city (or just doesn't exist).
    """
    pass


class UnexistingCellException(Exception):
    """
    Method was called for a cell that wasn't purchased for given
    business in current city (or just doesn't exist).
    """
    pass


class BusinessManager:
    """Manager of businesses in a city."""

    @lazy_property
    def _business_list(self):
        """
        Return dict of purchased businesses in a city.

        Can raise OutOfCityException.
        """
        page = get_page('business')
        if page.find(id='message', text='There are no businesses',
                     recursive=True):
            raise OutOfCityException

        business_name_list = [
                x.find('h3').string for x in
                page.find_all(attrs={'class': 'tabbertab'}, recursive=True)]
        business_list = {x: Business(x, page) for x in business_name_list}
        return business_list

    def __len__(self):
        return len(self._business_list)

    def __getitem__(self, key):
        return self._business_list[key]

    def __iter__(self):
        for business in self._business_list:
            yield business

    def __keytransform__(self, key):
        return key.lower()

    def __str__(self):
        return '%s: %s' % (str(BusinessManager), str(self._business_list))


class Business:
    """Actual business, i. e. bought in a city."""

    def __init__(self, name, page):
        """
        Save name of business and the businesses page to be parsed later.

        Can raise UnexistingBusinessException.
        """
        self.name = name
        self.page = page

    @lazy_property
    def _cell_list(self):
        """Return dict of purchased businesses in a city."""
        if name not in business_name_list:
            raise OutOfCityException
        if name not in (x.string for x in tabbernav.findall('li a')):
            raise UnexistingBusinessException

        container = page.find(attrs={'class': 'tabbernav'}, recursive=True)
        interface_cells = (
                .find('h3', text=re.compile(self.name, re.IGNORECASE))
                .parent()
                .find_all('td'))
        index_list = [
                re.search('swapinfo\((\d+),(\d+)\)', str(x.string)).groups()
                for x in interface_cells]
        #TODO: get data by indexes.

        return {x.find('a').string: Cell(x.find('a').string, page)
                for x in container('li')}

    def __len__(self):
        return len(self._cell_list)

    def __getitem__(self, key):
        return self._cell_list[key]

    def __iter__(self):
        for cell in self._cell_list:
            yield cell

    def __keytransform__(self, key):
        return key.lower()

    def __str__(self):
        return '%s: %s' % (str(Business), str(self._cell_list))


class Cell:
    """Business cell."""

    def __init__(self, number, page):
        """
        Save number of cell and the businesses page to be parsed later.

        Can raise UnexistingCellException.
        """
        self.number = number
        self.page = page

    @property
    def status(self):
        """
        Return status of given cell of given business.

        Possible statuses: (not purchased/free for use/in progress/
        ready for sale).
        """
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
