import time
import functools
import logging
from typing import Callable, Optional, List, Tuple
from pyrpio.i2c_register_device import I2CRegisterDevice
from pyrpio.i2c import I2CBase

log = logging.getLogger(__name__)

OutputEnableSetFunc = Optional[Callable[[bool], None]]
OutputEnableGetFunc = Optional[Callable[[], bool]]


class PCA9685:
    MODE1_REG_ADDR = 0x00
    MODE2_REG_ADDR = 0x01
    SUB_ADDR1_REG_ADDR = 0x02
    SUB_ADDR2_REG_ADDR = 0x03
    SUB_ADDR3_REG_ADDR = 0x04
    ALL_CALL_ADDR_REG_ADDR = 0x05
    CHANNEL_BASE_ADDR = 0x06

    def __init__(self, bus: I2CBase, address=0x20):
        self.address = address
        self.bus = bus
        self.i2c_reg = I2CRegisterDevice(bus, address, register_size=1, data_size=1)
        self._output_enable_setter: OutputEnableSetFunc = None
        self._output_enable_getter: OutputEnableGetFunc = None

    def get_register(self, register: int, mask: Optional[int] = None) -> int:
        ''' Get single byte register w/ optional mask. '''
        return self.i2c_reg.read_register(register, mask=mask)

    def set_register(self, register, value: int, mask: Optional[int] = None):
        ''' Set single byte register w/ optional mask. '''
        self.i2c_reg.write_register(register, value, mask=mask)

    def get_register_bit(self, register: int, bit: int) -> bool:
        ''' Get single bit from register. '''
        mask = 1 << bit
        value = self.get_register(register, mask)
        return bool(value >> bit)

    def set_register_bit(self, register: int, bit: int, on: bool):
        ''' Set single bit of a register. '''
        mask = 1 << bit
        pvalue = self.get_register(register, ~mask)
        self.set_register(register, pvalue | (int(on) << bit))

    def set_register_bits(self, register: int, bits: List[int], ons: List[bool]):
        ''' Set single bit of a register. '''
        mask = functools.reduce(lambda a, b: a | (1 << b), bits, 0)
        value = functools.reduce(lambda a, b: a | b, (int(on) << bit for on, bit in zip(ons, bits)))
        pvalue = self.get_register(register, ~mask)
        self.set_register(register, pvalue | value)

    def _get_channel_base_address(self, ch: int) -> int:
        ''' Get channel base register address. '''
        return PCA9685.CHANNEL_BASE_ADDR + 4*ch

    def set_output_enable_setter(self, setter: OutputEnableSetFunc = None):
        ''' Provide callable to toggle physical oe pin. '''
        self._output_enable_setter = setter

    def set_output_enable_getter(self, getter: OutputEnableGetFunc = None):
        ''' Provide callable to get physical oe pin state. '''
        self._output_enable_getter = getter

    @property
    def output_enable(self) -> bool:
        ''' Get state of output enable pin.
            NOTE: Requires calling `set_output_enable_getter` otherwise false will be returned.
        '''
        if self._output_enable_getter:
            return self._output_enable_getter()
        return False

    @output_enable.setter
    def set_output_enable(self, enable: bool):
        ''' Set output enable pin state.
            NOTE: Requires calling `set_output_enable_setter` otherwise no action is performed.
        '''
        if self._output_enable_setter:
            self._output_enable_setter(enable)

    def soft_reset(self):
        ''' Perform soft reset by writing 0x06 to i2c address 0x00. '''
        self.bus.set_address(0x00)
        self.bus.write(data=bytes([0x06]))
        self.bus.set_address(self.address)

    @property
    def pwm_prescale(self):
        ''' Get PWM prescale value [min=0x03 max=0xFF].
            prescale = round(osc_clk / (4096 x update_rate)) - 1
        '''
        return self.get_register(register=0xFE)

    @pwm_prescale.setter
    def pwm_prescale(self, prescale: int):
        ''' Set PWM prescale value.
            prescale = round(osc_clk / (4096 x update_rate)) - 1
        '''
        prescale = min(max(3, prescale), 255)
        self.set_register(register=0xFE, value=prescale)

    @property
    def mode1(self) -> int:
        ''' Get mode1 register value. '''
        return self.get_register(register=PCA9685.MODE1_REG_ADDR)

    @mode1.setter
    def mode1(self, value: int):
        ''' Set mode1 register value. '''
        return self.set_register(register=PCA9685.MODE1_REG_ADDR, value=value)

    @property
    def mode2(self) -> int:
        ''' Get mode2 register value. '''
        return self.get_register(register=PCA9685.MODE2_REG_ADDR)

    @mode2.setter
    def mode2(self, value: int):
        ''' Set mode2 register value. '''
        return self.set_register(register=PCA9685.MODE2_REG_ADDR, value=value)

    @property
    def subaddr1(self) -> int:
        ''' Get subaddress1 register value. '''
        return self.get_register(register=PCA9685.SUB_ADDR1_REG_ADDR)

    @subaddr1.setter
    def subaddr1(self, value: int):
        ''' Set subaddress1 register value. '''
        return self.set_register(register=PCA9685.SUB_ADDR1_REG_ADDR, value=value)

    @property
    def subaddr2(self) -> int:
        ''' Get subaddress2 register value. '''
        return self.get_register(register=PCA9685.SUB_ADDR2_REG_ADDR)

    @subaddr2.setter
    def subaddr2(self, value: int):
        ''' Set subaddress2 register value. '''
        return self.set_register(register=PCA9685.SUB_ADDR2_REG_ADDR, value=value)

    @property
    def subaddr3(self) -> int:
        ''' Get subaddress3 register value. '''
        return self.get_register(register=PCA9685.SUB_ADDR3_REG_ADDR)

    @subaddr3.setter
    def subaddr3(self, value: int):
        ''' Set subaddress3 register value. '''
        return self.set_register(register=PCA9685.SUB_ADDR3_REG_ADDR, value=value)

    @property
    def allcalladdr(self) -> int:
        ''' Get all-call address register value. '''
        return self.get_register(register=PCA9685.ALL_CALL_ADDR_REG_ADDR)

    @allcalladdr.setter
    def allcalladdr(self, value: int):
        ''' Set all-call address register value. '''
        return self.set_register(register=PCA9685.ALL_CALL_ADDR_REG_ADDR, value=value)

    @property
    def logic_restart_state(self) -> bool:
        ''' Get logic restart value. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=7)

    def restart_logic(self):
        ''' Restart chip logic. '''
        self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=7, on=True)

    @property
    def autoincrement(self) -> bool:
        ''' Get autoincrement i2c addresses flag. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=5)

    @autoincrement.setter
    def autoincrement(self, on: bool):
        ''' Set autoincrement i2c addresses flag. '''
        self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=5, on=on)

    @property
    def sleep(self) -> bool:
        ''' Get chip sleep mode. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=4)

    @sleep.setter
    def sleep(self, on: bool):
        ''' Set chip sleep mode. '''
        self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=4, on=on)

    @property
    def use_external_clock(self) -> bool:
        ''' Get external clock source flag. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=6)

    @use_external_clock.setter
    def use_external_clock(self, enable: bool):
        ''' Set whether external clock source or internal is used. '''

        if self.use_external_clock == enable:
            return
        if not enable:
            self.soft_reset()
        elif self.sleep:
            self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=6, on=True)
        else:
            self.sleep = True
            self.set_register_bits(register=PCA9685.MODE1_REG_ADDR, bits=[4, 6], ons=[True, True])
            time.sleep(500e-6)
            self.sleep = False
            time.sleep(500e-6)

    @property
    def subaddr1_set(self) -> bool:
        ''' Get if chip responds to subaddress 1. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=3)

    @subaddr1_set.setter
    def subaddr1_set(self, on: bool):
        ''' Set if chip responds to subaddress 1. '''
        return self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=3, on=on)

    @property
    def subaddr2_set(self) -> bool:
        ''' Get if chip responds to subaddress 2. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=2)

    @subaddr2_set.setter
    def subaddr2_set(self, on: bool):
        ''' Set if chip responds to subaddress 2. '''
        return self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=2, on=on)

    @property
    def subaddr3_set(self) -> bool:
        ''' Get if chip responds to subaddress 3. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=1)

    @subaddr3_set.setter
    def subaddr3_set(self, on: bool):
        ''' Set if chip responds to subaddress 3. '''
        return self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=1, on=on)

    @property
    def allcalladdr_set(self) -> bool:
        ''' Get if chip responds to All Call address. '''
        return self.get_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=0)

    @allcalladdr_set.setter
    def allcalladdr_set(self, on: bool):
        ''' Set if chip responds to All Call address. '''
        return self.set_register_bit(register=PCA9685.MODE1_REG_ADDR, bit=0, on=on)

    @property
    def output_invert(self) -> bool:
        ''' Get if output logic state is inverted. '''
        return self.get_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=4)

    @output_invert.setter
    def output_invert(self, on: bool):
        ''' Set if output logic state is inverted. '''
        return self.set_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=4, on=on)

    @property
    def output_change(self) -> bool:
        ''' Get if outputs change on STOP command [0] or ACK [1]. '''
        return self.get_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=3)

    @output_change.setter
    def output_change(self, on: bool):
        ''' Set if outputs change on STOP command [0] or ACK [1]. '''
        return self.set_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=3, on=on)

    @property
    def output_drive(self) -> int:
        ''' Get output drive mode: 0 -> open-drain, 1 -> totem pole. '''
        return int(self.get_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=2))

    @output_drive.setter
    def output_drive(self, drive: int):
        ''' Set output drive mode: 0 -> open-drain, 1 -> totem pole. '''
        return self.set_register_bit(register=PCA9685.MODE2_REG_ADDR, bit=2, on=bool(drive))

    @property
    def output_not_enable_mode(self) -> int:
        ''' Get output not enable mode. LEDn output when !OE = 1
            00: LEDn = 0
            01: LEDn = 1 when OUTDRV = 1 else high-impedance
            1X: LEDn = high-impedance
        '''
        return self.get_register(register=PCA9685.MODE2_REG_ADDR, mask=0x3)

    @output_not_enable_mode.setter
    def output_not_enable_mode(self, mode: int):
        ''' Set output not enable mode. '''
        return self.set_register(register=PCA9685.MODE2_REG_ADDR, value=mode, mask=0x3)

    def get_pwm_frequency(self, ref_freq: float = 25E6) -> float:
        ''' Get PWM frequency based on prescale and ref freq (Hz). '''
        return ref_freq / (4096.0*(self.pwm_prescale + 1.0))

    def set_pwm_frequency(self, freq: float, ref_freq: float = 25E6):
        ''' Set PWM prescale based on desired frequency in Hz. '''
        self.pwm_prescale = int(ref_freq / 4096.0 / freq + 0.5)

    def get_channel_on_counter(self, ch: int) -> Tuple[int, bool]:
        ''' Set channel on counter [0 - 4095]. Can also fully turn on channel. '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        lsb = self.get_register(register=ch_base_addr+0)
        msb = self.get_register(register=ch_base_addr+1)
        value = ((msb & 0x0F) << 8) | (lsb & 0xFF)
        full_on = bool(msb & 0x10)
        return value, full_on

    def get_channel_off_counter(self, ch: int) -> Tuple[int, bool]:
        ''' Set channel on counter [0 - 4095]. Can also fully turn on channel. '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        lsb = self.get_register(register=ch_base_addr+2)
        msb = self.get_register(register=ch_base_addr+3)
        value = ((msb & 0x0F) << 8) | (lsb & 0xFF)
        full_on = bool(msb & 0x10)
        return value, full_on

    def set_channel_on_counter(self, ch: int, on: int, full_on: bool):
        ''' Set channel on counter [0 - 4095]. Can also fully turn on channel. '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        self.set_register(register=ch_base_addr+0, value=on & 0xFF)  # ON LSB
        self.set_register(register=ch_base_addr+1, value=((on >> 8) & 0x0F) | (int(full_on) << 4))  # ON MSB

    def set_channel_off_counter(self, ch: int, off: int, full_off: bool):
        ''' Set channel off counter [0 - 4095]. Can also fully turn off channel. '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        self.set_register(register=ch_base_addr+2, value=off & 0xFF)  # OFF LSB
        self.set_register(register=ch_base_addr+3, value=((off >> 8) & 0x0F) | (int(full_off) << 4))  # OFF MSB

    def set_channel_full_on(self, ch: int, on: bool):
        ''' Set channel fully on (ignores on and off counters). '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        self.set_register_bit(register=ch_base_addr+1, bit=4, on=on)

    def set_channel_full_off(self, ch: int, off: bool):
        ''' Set channel fully off (ignores on and off counters). '''
        ch_base_addr = self._get_channel_base_address(ch=ch)
        self.set_register_bit(register=ch_base_addr+3, bit=4, on=off)

    def set_channel_counters(self, ch: int, on: int, off: int, full_on: bool, full_off: bool):
        ''' Set channels on and off counter. '''
        self.set_channel_on_counter(ch=ch, on=on, full_on=full_on)
        self.set_channel_off_counter(ch=ch, off=off, full_off=full_off)

    def get_channel_pwm(self, ch: int) -> Tuple[float, float]:
        ''' Get channels PWM duty cycle and delay. '''
        delay_cycles, full_on = self.get_channel_on_counter(ch=ch)
        off_cycles, full_off = self.get_channel_off_counter(ch=ch)
        if delay_cycles + (off_cycles - delay_cycles + 1) >= 4096 or off_cycles < delay_cycles:
            off_cycles += 4096
        on_cycles = off_cycles - delay_cycles + 1
        log.debug(
            'delay=%i, on=%i (full=%i), off=%i (full=%i)',
            delay_cycles, on_cycles, full_on, off_cycles, full_off
        )
        duty_cycle = 1 if full_on else 0 if full_off else round(on_cycles/4096, 3)
        delay = round((delay_cycles+1)/4096, 3)
        return duty_cycle, delay

    def set_channel_pwm(self, ch: int, duty_cycle: float, delay: float = 0):
        ''' Set channel counters based on desired duty cycle and delay.
            Args:
                duty_cycle: PWM duty cycle fraction [0, 1]
                delay: Fractional delay [0, 1]
        '''
        duty_cycle = max(min(duty_cycle, 1), 0)
        delay = max(min(delay, 1), 0)
        full_on = abs(1 - duty_cycle) <= 1e-3
        full_off = duty_cycle <= 1e-3
        if delay is None:
            delay = 0
        delay_cycles = max(0, round(delay*4096) - 1)
        on_cycles = max(0, round(duty_cycle*4096))
        off_cycles = delay_cycles + on_cycles
        off_cycles = max(0, off_cycles - 1 if off_cycles <= 4096 else off_cycles - 4096)
        log.debug(
            'delay=%i, on=%i (full=%i), off=%i (full=%i)',
            delay_cycles, on_cycles, full_on, off_cycles, full_off
        )
        if delay_cycles == off_cycles and not full_on and not full_off:
            raise ValueError('on counter and off counter cant be same value')
        self.set_channel_on_counter(ch=ch, on=delay_cycles, full_on=full_on)
        self.set_channel_off_counter(ch=ch, off=off_cycles, full_off=full_off)

    def disable_channel(self, ch: int):
        ''' Disable channel by setting LED off bit high'''
        self.set_channel_full_off(ch=ch, off=True)
