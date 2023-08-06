from ...__private.utilities import *


class DataStore(ABC):
    @abstractmethod
    def __getitem__(self, item: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, item: str) -> bool:
        raise NotImplementedError


class SimpleRAMDataStore(DataStore):
    def __init__(self):
        self._storage: Dict[str, Any] = dict()

    def __getitem__(self, item: str) -> Optional[Any]:
        return self._storage.get(item, None)

    def __setitem__(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def __contains__(self, item: str) -> bool:
        return item in self._storage
