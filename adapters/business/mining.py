"""Adapter for mining business."""
from adapters.business.business_base import Business
from adapters.business.business_manager import BusinessManager


class MiningBusiness(Business):
    """Business subclass that implements specifics in Mine usage."""

    """Special constant BusinessManager uses to select Business subclass."""
    _business_name = 'Mine'

BusinessManager.register_business(MiningBusiness)
