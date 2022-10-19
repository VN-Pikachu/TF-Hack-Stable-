from abc import abstractmethod
from typing import Iterable, List
from dataclasses import dataclass
from csv import DictReader


@dataclass
class TankData:
    id: int
    name: str
    hp: float
    speed: float
    turet: float
    acceleration: float
    turn: float
    reload: float


class TankDataStorage:
    @abstractmethod
    def load(self) -> Iterable[TankData]:
        return []


class TankDataCSV(TankDataStorage):
    def __init__(self, data_path: str):
        self.__data_path = data_path

    def load(self) -> Iterable[TankData]:
        stat_names = ("hp", "speed", "turet", "acceleration", "turn", "reload")
        with open(self.__data_path) as file:
            reader = DictReader(file)
            for row in reader:
                stats = {name: float(row[name]) for name in stat_names}
                yield TankData(id=int(row["id"]), name=row["name"], **stats)


class AddressData:
    def __init__(self, data_path: str):
        self.__data_path = data_path

    def load(self) -> Iterable[int]:
        with open(self.__data_path) as file:
            for addr in file:
                yield int(addr.rstrip("\n"), 16)
