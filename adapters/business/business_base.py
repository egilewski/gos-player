"""Adapter for businesses."""
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


class Business:
    """Abstract bought in a city business."""

    def __init__(self, page):
        """
        Save businesses page to be parsed later.

        Can raise UnexistingBusinessException.
        """
        self.page = page

    @lazy_property
    def _cell_list(self):
        """Return dict of purchased cells of the business in the city."""
        business_container = self.page.find(attrs={'class': 'tabbernav'},
                                       recursive=True)
        if not business_container:
            raise OutOfCityException

        business_name_list = {x.string.lower(): x for x in container('h3')}
        if self._business_name not in business_name_list:
            raise UnexistingBusinessException

        interface_cells = business_titles[self._business_name].parent().find_all('td')
        index_list = [
                re.search('swapinfo\((\d+),(\d+)\)', str(x.string)).groups()
                for x in interface_cells]
        #TODO: get data by indices.

        return [Cell(x.find('a').string, page) for x in container('li')]

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


class UnsupportedBusiness(Business):
    """
    Special business type for unsupported businesses.

    Used when no class to support a business found.
    """
    _business_name = 'Unsupported'

    def __init__(self, *args, **kwargs):
        pass

    @property
    def _cell_list(self):
        return []