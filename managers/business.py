"""Adapter for businesses and related stuff."""
import game_connector


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

    @property
    def _business_list(self):
        """Return full list of purchased businesses in a city.
        Can raise OutOfCityException."""
        try:
            self.business_list
        except NameError:
            page = game_connector.get_page('business')
            if page.find(id='message', text='There are no businesses',
                         recoursive=True):
                raise OutOfCityException

            container = page.find(attrs={'class': 'tabbernav'},
                                  recoursive=True)
            self.business_list = [x.find('a').string for x in container('li')]

        return self.business_list

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

    def __contains__(self, item):
        retirn item in _business_list


class Business:
        """Can raise OutOfCityException, NoSuchBusiness, NoSuchCell."""
    pass


class Cell:
    """Business cell."""

    def get_business_cell_status(self):
        """Return status of given cell of given business.
        Possible statuses: (not purchased/free for use/in progress/
        ready for sale)."""
        pass

    def get_business_cell_last_process(self):
        """Return dict of last process info."""
        pass

    def release_business_cell(self):
        """Sell or release in another way result of finished process."""
        pass

    def execute(self, process):
        """Start process by name."""
        pass
