"""Adapter for mining business."""
from adapters.business.business_base import Business


class MiningBusiness(Business):
    """Business subclass that implements specifics in Mine usage."""

    """Special constant BusinessManager uses to select Business subclass."""
    _business_name = 'Mine'

Business.register_business(MiningBusiness)
