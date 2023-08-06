from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def as_dict(self):
        raise NotImplementedError
