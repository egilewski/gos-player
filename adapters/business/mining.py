"""Adapter for mining business."""
from adapters.business import business_cell


class MiningCell(business_cell.Cell):
    """Cell handler that implements specifics in Mine usage."""

    _cell_type = 'Mine'
    """Special constant CellFactory uses to select Cell handler."""
business_cell.CellLibrary.register(MiningCell)
