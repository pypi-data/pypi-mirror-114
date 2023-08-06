import time
from typing import List, Union, Optional
from contextlib import contextmanager
from functools import reduce
from pyrpio.i2c import I2CBase

class PCA9543A:
    """The PCA9543A is a dual 2 bidirectional translating switch controlled by the I2C bus.
    """

    def __init__(self, bus: I2CBase, address: int = 0x70):
        """Constructor

        Args:
            bus: Subclass of I2CBase
            address: I2C address of device. Defaults to 0x70.
        """
        self.address = address
        self.bus = bus

    @property
    def num_lanes(self) -> int:
        """Get number of downstream lanes.

        Returns:
            int: number of downstream lanes
        """
        return 2

    @property
    def lanes(self) -> List[int]:
        """Get list of downstream lanes.

        Returns:
            List[int]: Downstream lanes
        """
        return [0, 1]

    def compute_value_from_lanes(self, lanes: Union[int, List[int]]) -> int:
        """Compute control register value from lanes.

        Args:
            lanes (Union[int, List[int]]): Target lanes

        Returns:
            int: Control register value
        """
        lanes = [lanes] if isinstance(lanes, int) else lanes
        return reduce(lambda acc, val: acc | (1 << val), lanes or [], 0)

    def get_control_register(self) -> int:
        """Get mux control register value.

        Returns:
            int: Control register
        """
        self.bus.set_address(self.address)
        return int.from_bytes(self.bus.read(length=1), byteorder='big')

    def set_control_register(self, value: int):
        """Set mux control register value.

        Args:
            value (int): Control register value
        """
        self.bus.set_address(self.address)
        self.bus.write(bytes([value]))

    def set_lanes(self, lanes: Union[int, List[int]]):
        """Set active downstream lanes.

        Args:
            lanes (Union[int, List[int]]): Downstream i2c lanes to enable
        """
        self.set_control_register(self.compute_value_from_lanes(lanes=lanes))
        time.sleep(0.05)

    def get_lanes(self) -> List[int]:
        """Get active downstream lanes.

        Returns:
            List[int]: Lanes
        """
        lanes = []
        value = self.get_control_register() & 0x3
        for lane in range(self.num_lanes):
            if value & (1 << lane):
                lanes.append(lane)
        return lanes

    def get_lane_interrupt(self, lane: int) -> bool:
        """Get interrupt flag for given lane.

        Args:
            lane (int): Downstream i2c lane

        Returns:
            bool: If interrupt flag is set
        """
        return bool(self.get_control_register() & (1 << (lane + 4)))

    def clear_lanes(self):
        """Clear all active downstream lanes.
        """
        self.set_control_register(value=0)

    @contextmanager
    def open_lanes(self, lanes: Optional[List[int]] = None, release: bool = False):
        """Open lanes only while in context block. Attempts to be re-entrant by only setting if active
        lanes are different and restores to what they were.
        Args:
            lanes (Optional[List[int]], optional): Downstream i2c lanes. Defaults to None.
            release (bool, optional): If True, will force release all lanes on exit. Defaults to False.

        Yields:
            int: Command register value
        """
        pvalue = 0
        value = self.compute_value_from_lanes(lanes)
        try:
            pvalue = self.get_control_register() & 0x3
            if pvalue != value:
                self.set_control_register(value=value)
            yield value
        finally:
            if release:
                self.clear_lanes()
            elif pvalue != value:
                self.set_control_register(value=pvalue)
