"""Adapter for mining business."""
from adapters.business import business_base


class MiningBusiness(business_base.Business):
    """Business subclass that implements specifics in Mine usage."""
    pass
business_base.BusinessLibrary.register(MiningBusiness)
