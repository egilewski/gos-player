"""Adapter for mining business."""
from adapters.business import business_base


class MiningBusiness(business_base.Business):
    """Business subclass that implements specifics in Mine usage."""

    """Special constant BusinessManager uses to select Business subclass."""
    _business_name = 'Mine'
business_base.BusinessLibrary.register(MiningBusiness)
