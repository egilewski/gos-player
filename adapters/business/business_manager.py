"""Manager for adapters for businessess."""
from game_connector import get_page
from utils import lazy_property
from adapters.business import business_base


class UnsupportedBusinessException(Exception):
    """Business adapter for a business not found."""
    pass


class BusinessManager:
    """Manager of businesses in a city."""
    _registered_businesses = {}

    @lazy_property
    def _business_list(self):
        """
        Return dict of purchased businesses in a city.

        Values of the dict are of subclasses of class Business.
        Can raise OutOfCityException.
        """
        page = get_page('business')
        if page.find(id='message', text='There are no businesses',
                     recursive=True):
            raise business_base.OutOfCityException

        business_name_list = [
                x.find('h3').string for x in
                page.find_all(attrs={'class': 'tabbertab'}, recursive=True)]
        business_dict = {x: business_base.Business(x, page)
                         for x in business_name_list}
        return business_dict

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
