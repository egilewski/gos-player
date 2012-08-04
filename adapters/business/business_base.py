"""Business handler."""
import re
from html.parser import HTMLParser
from utils import lazy_property
from adapters.business.business_cell import Cell


class OutOfCityException(Exception):
    """Method that can be used only in a city was called in a wilderness."""
    pass


class UnexistingBusinessException(Exception):
    """
    Method was called for business that wasn't purchased in current
    city.
    """
    pass


class Business:
    """
    Representation of one business bought in current city.
    """

    def __init__(self, business_name, page):
        """
        Save businesses page to be parsed later.
        """
        self._page = page

    @lazy_property
    def _cell_id_list(self):
        """
        Return list of cell compound IDs.

        Can raise OutOfCityException and UnexistingBusinessException.
        """
        business_container = self._page.find(attrs={'class': 'tabber'},
                                       recursive=True)
        if not business_container:
            raise OutOfCityException

        business_name_list = {x.string: x
                              for x in business_container.find_all('h3')}
        if self._business_name not in business_name_list:
            raise UnexistingBusinessException

        interface_cells = (business_name_list[self._business_name]
                           .parent.find_all('td'))
        index_list = []
        for cell in interface_cells:
            match = re.search('swapinfo\((\d+),(\d+)\)', str(cell))
            if match:
                index_list.append((int(match.group(1)), int(match.group(2))))
        return index_list

    @lazy_property
    def _raw_cell_list(self):
        """
        Return list of HTML prepared to be inserted into interface info
        cell.

        Unexisting cells are excluded from the list.
        """
        infocell_list = []
        for id0, id1 in self._cell_id_list:
            match = re.search(
                    'bstats\[%d\]\[%d\] *= *["\']([^\n]*)["\']' % (id0, id1),
                    str(self._page))
            if match:
                cell_string = HTMLParser().unescape(match.group(1))
                infocell_list.append(cell_string)
        return infocell_list

    @lazy_property
    def _cell_list(self):
        """
        Return list of Cell objects representing purchased of the
        business in the city.
        """
        return [Cell(x) for x in self._raw_cell_list]

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
