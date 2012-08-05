"""Cell base handler and it's helper classes."""
import re
from utils import lazy_property


class UnexistingCellException(Exception):
    """
    Method was called for cell that wasn't purchased for given
    business in current city.
    """
    pass


class CellHandlerNotFoundException(Exception):
    """
    No handler for business found.

    Shouldn't be raised, as there is UnsupportedBusiness handler."""
    pass


class CellLibrary:
    """
    Collection of cell handler classes.

    Cell handlers should be registered with register() method.
    get_handler() method returns appropriate handler among registered.

    Handler with higer priority is returned when multiple found.

    Shouldn't be instantiated.
    """

    _cell_list = []
    """
    List of registered cell handlers.

    Item format: (cell_type, priority).
    """

    def __new__(cls):
        """Simple protection from Jimmy."""
        raise Exception("%s shouldn't be instantiated" % cls.__name__)

    @classmethod
    def register(cls, cell_type, priority=0):
        """
        Save cell handler class to search among later.

        cell_type should have static/classmethod supports() with
        exactly one mandatory argument. Return value will be casted to
        boolean.
        """
        cls._cell_list.append((cell_type, priority))

    @classmethod
    def get_handler(cls, cell_type):
        """Return appropriate cell handler class by cell type."""
        cls._business_list.sort(key=lambda a: a[1], reverse=True)
        for cell_class, priority in cls._cell_list:
            if cell_class.supports(cell_type):
                return cell_class
        raise CellHandlerNotFoundException


class CellFactory(type):
    """
    Factory for instantiating registered cell driver instead of object
    of class Cell.
    """

    @classmethod
    def __call__(cls, cell_type, page):
        """
        Find and instantiate registered cell handler class that claims
        to support cell of given type.
        """
        handler_class = CellLibrary.get_handler(cell_type)
        return super().__call__(handler_class, cell_type, page)


class Cell(metaclass=CellFactory):
    """
    Business cell.

    On instantiation creates and returns object of one of cell handler
    classess registered in CellLibrary.
    """

    _cell_type = ''
    """
    Name of cell, default implementation of supports() method reports to
    accept.

    With value casted to boolean false it won't report to support
    anything.
    """

    def __init__(self, info):
        """
        Save businesses page to be parsed later.

        Can raise UnexistingCellException.
        """
        #TODO: delete this after writing _parse_info.
        self._raw_info = info
        self._info = self._parse_info(info)

    def _parse_info(self, cell_raw_info):
        """Return dict of cell data."""
        #TODO: Find out if this can be used for at least Mine and Farm.
        #TODO: If not, move this code to concrete handlers and left this empty.
        cell_info = {}
        cell_info['name'] = re.search(
                "^<font class='littletext'>([^\d]*) ", cell_raw_info).group(1)
        cell_info['number'] = int(re.search(
                "^<font class='littletext'>[^\d]*(\d*)", cell_raw_info)
                .group(1))
        return cell_info

    @classmethod
    def supports(cls, cell_type):
        return cls._cell_type and cell_type == cls._cell_type

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


class UnsupportedCell(Cell):
    """
    Special cell handler for unsupported cell types.

    Used when no class to support a cell type was found
    (i. e. has low priority).

    Doesn't do anything.
    """

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def supports(cls, business_name):
        return True

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
CellLibrary.register(UnsupportedCell, -1000)
