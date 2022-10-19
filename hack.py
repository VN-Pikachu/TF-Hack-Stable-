from typing import Dict, Iterable, cast

from memory import Memory
from storage import AddressData, TankDataStorage, TankDataCSV, TankData
from structure import ClassFactory, Struct


class UnitSettings:
    def __init__(self, mem: Memory, settings: Struct):
        self.__mem = mem
        self.__settings = settings

    def set(self, path: Iterable[str], value: float) -> None:
        if value == -1:
            return
        self.__mem.write_float(self.__settings.find(*path), value)

    def get(self, path: Iterable[str]) -> float:
        return self.__mem.read_float(self.__settings.find(*path))


class TankDataHacker:
    def __init__(self, process_name: str, data_path: str, address_path: str):
        self.memory: Memory = Memory(process_name)
        self.factory: ClassFactory = ClassFactory()
        self.tanks_data: TankDataStorage = TankDataCSV(data_path)
        self.unit_addr_data = AddressData(address_path)
        self.tank_map: Dict[int, TankData] = {}

        self.__create_tank_map()

    def __create_tank_map(self) -> None:
        for data in self.tanks_data.load():
            self.tank_map[data.id] = data

    def hack(self, unit_addr: int) -> None:
        unit = self.factory.make_unit()
        self.memory.set_addr(unit, unit_addr)

        unit_id = self.memory.read_int(unit.find("id"))
        # WARNING: handle case when the ID of unit is not in database
        # if unit_id not in tank_map:
        #     continue
        data = self.tank_map[unit_id]
        self.sync(unit, data)

    def sync(self, unit: Struct, data: TankData) -> None:
        settings = cast(Struct, unit["settings"])
        unit_settings = UnitSettings(self.memory, settings)

        unit_settings.set(("hp", "current"), data.hp)
        unit_settings.set(("hp", "max"), data.hp)
        unit_settings.set(("speed", "current"), data.speed)
        unit_settings.set(("speed", "max"), data.speed)
        unit_settings.set(("turet", "current"), data.turet)
        unit_settings.set(("turet", "max"), data.turet)
        unit_settings.set(("acceleration", "min"), data.acceleration - 2)
        unit_settings.set(("acceleration", "current"), data.acceleration)
        unit_settings.set(("acceleration", "max"), data.acceleration)
        unit_settings.set(("turn", "current"), data.turn)
        unit_settings.set(("turn", "max"), data.turn)
        unit_settings.set(("reload", "current"), data.reload)
        unit_settings.set(("reload", "max"), data.reload)
        damage = self.memory.read_float(settings.find("damage", "max"))
        unit_settings.set(("damage", "min"), damage - 20.0)
        # TODO: set damage
        # unit_settings.set(("damage", "min"), 0)

    def run(self)->None:
        for unit_addr in self.unit_addr_data.load():
            self.hack(unit_addr)
