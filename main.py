import os
from hack import TankDataHacker

PROCESS_NAME = "TankForce.exe"
DATA_PATH = os.path.join("data", "data.csv")
ADDRESS_PATH = os.path.join("data", "addresses.txt")

hacker = TankDataHacker(PROCESS_NAME, DATA_PATH, ADDRESS_PATH)
hacker.run()