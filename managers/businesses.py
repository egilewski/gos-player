"""Adapter for businesses and related stuff."""


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


class BusinessesManager:
    """Manager of businesses in a city."""

    @property
    def _businesses_list(self):
        """Return full list of purchased businesses in a city.
        Can raise OutOfCityException."""
        pass

    def __len__(self):
        return len(_businesses_list)

    def __getitem__(self, key):
        return _businesses_list[key]

    def __iter__(self):
        for business in _businesses_list:
            yield business

    def __reversed__(self):
        for business in reverse(_businesses_list):
            yield business

    def __contains__(self, item):
        retirn item in _businesses_list


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
