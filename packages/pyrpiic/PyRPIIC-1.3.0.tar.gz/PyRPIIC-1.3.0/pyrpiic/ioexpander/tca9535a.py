from pyrpio.i2c import I2CBase
from .tca6416a import TCA6416A


class TCA9535A(TCA6416A):
    def __init__(self, bus: I2CBase, address: int):
        super().__init__(bus=bus, address=address)
