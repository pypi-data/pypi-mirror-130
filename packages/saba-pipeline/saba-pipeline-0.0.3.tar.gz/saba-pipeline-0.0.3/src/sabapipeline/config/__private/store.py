from ...__private.utilities import *


class DataStore(ABC):
    @abstractmethod
    def get_value(self, key: str) -> Optional[Any]:
        raise NotImplementedError()

    @abstractmethod
    def set_value(self, key: str, value: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def contains(self, key: str) -> bool:
        raise NotImplementedError()

    def __getitem__(self, item: str) -> Optional[Any]:
        return self.get_value(item)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set_value(key, value)

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def get_branch(self, prefix: str, value_generator: Callable[[str], Any] = None):
        return DataStoreBranch(self, prefix, value_generator)


class DataStoreBranch(DataStore):
    def __init__(self,
                 parent_data_store: DataStore,
                 prefix: str,
                 value_generator: Callable[[str], Any]
                 ):
        super().__init__()
        self._parent_data_store = parent_data_store
        self._prefix = prefix
        self._value_generator = value_generator

    def get_value(self, key: str) -> Optional[Any]:
        result = self._parent_data_store.get_value(self._prefix + key)
        if result is None and self._value_generator is not None:
            result = self._value_generator(key)
            self.set_value(key, result)
        return result

    def set_value(self, key: str, value: Any) -> None:
        self._parent_data_store.set_value(self._prefix + key, value)

    def contains(self, key: str) -> bool:
        return self._parent_data_store.contains(self._prefix + key)


class SimpleRAMDataStore(DataStore):
    def __init__(self):
        super().__init__()
        self._storage: Dict[str, Any] = dict()

    def get_value(self, key: str) -> Optional[Any]:
        return self._storage.get(key, None)

    def set_value(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def contains(self, key: str) -> bool:
        return key in self._storage
