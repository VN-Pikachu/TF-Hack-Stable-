from __future__ import annotations
from typing import Dict, Generator, List, Optional, MutableMapping
from copy import deepcopy


class Base:
    def __init__(self, offsets: Optional[List[int]] = None, addr: int = -1, name: str = ""):
        self.parent: Optional[Base] = None
        self.offsets = offsets
        self._properties: Dict[str, Base] = {}
        self.addr = addr
        self.name = name

    @property
    def offsets(self) -> List[int]:
        return self._offsets

    @offsets.setter
    def offsets(self, value: Optional[List[int]]) -> None:
        self._offsets = [] if value is None else value


class Float(Base):
    pass


class Int(Base):
    pass


class Struct(Base, MutableMapping[str, Base]):
    def find(self, *path: str) -> Base:
        obj = self
        # TODO: Better exception message description
        for key in path:
            if not isinstance(obj, Struct):
                raise ValueError("path is unreachable")
            if key not in obj:
                raise ValueError("Invalid key in path")
            obj = obj[key]
        return obj

    def __getitem__(self, key: str) -> Base:
        return self._properties[key]

    def __setitem__(self, key: str, value: Base) -> None:
        value.parent = self
        self._properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self._properties[key]

    def __iter__(self) -> Generator[str, None, None]:
        yield from self._properties.keys()

    def __len__(self) -> int:
        return len(self._properties)


class ClassFactory:
    def __init__(self):
        self.__init_krampus()
        self.__init_settings()
        self.__init_unit()

    def make_krampus(
        self, offsets: Optional[List[int]] = None, addr: int = -1
    ) -> Struct:
        return self.__make_prototype(self._krampus, offsets, addr)

    def make_settings(
        self, offsets: Optional[List[int]] = None, addr: int = -1
    ) -> Struct:
        return self.__make_prototype(self._settings, offsets, addr)

    def make_unit(self, offsets: Optional[List[int]] = None, addr: int = -1) -> Struct:
        return self.__make_prototype(self._unit, offsets, addr)

    def __make_prototype(
        self, prototype: Struct, offsets: Optional[List[int]] = None, addr: int = -1
    ) -> Struct:
        instance = deepcopy(prototype)
        instance.offsets = offsets
        instance.addr = addr
        return instance

    def __init_krampus(self) -> None:
        krampus = Struct(name="krampus")
        krampus["min"] = Float([0x10], name="min")
        krampus["current"] = Float([0x14], name="current")
        krampus["max"] = Float([0x18], name="max")
        self._krampus = krampus

    def __init_settings(self) -> None:
        settings = Struct(name="settings")
        settings["hp"] = self.make_krampus([0x10])
        settings["speed"] = self.make_krampus([0x28])
        settings["turet"] = self.make_krampus([0x30])
        settings["acceleration"] = self.make_krampus([0x38])
        settings["turn"] = self.make_krampus([0x40])
        settings["reload"] = self.make_krampus([0x58, 0x10, 0x30])
        settings["damage"] = self.make_krampus([0x58, 0x10, 0x40])
        self._settings = settings

    def __init_unit(self) -> None:
        unit = Struct(name="unit")
        # TODO: right offset for ID in cheat engine
        unit["id"] = Float([0x10], name="id")
        unit["settings"] = self.make_settings([0x90])
        self._unit = unit
