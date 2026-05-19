from src.config import settings
from src.serial.hardware import HardwareSerialService
from src.serial.mock import MockSerialService

class AppController:
    """
    The central controller for the application.
    Manages register state, serial service lifecycle, and coordinates GUI requests.
    """

    def __init__(self):
        # Initialize the Register Cache to 0x00 as per Spec 6.1
        self.cache = {reg.address: 0x00 for reg in settings.REGISTERS}
        
        # Initialize the appropriate Serial Service
        if settings.MOCK_MODE:
            self.serial_service = MockSerialService()
        else:
            # This may raise ConnectionError, handled by main.py
            self.serial_service = HardwareSerialService()

    def startup_sync(self):
        """
        Transmits all initial register values (0x00) to the hardware.
        Should be called after the GUI is ready but before user interaction begins.
        """
        for reg in settings.REGISTERS:
            # We use the direct serial write here to avoid cache redundancy 
            # and ensure a clean startup state.
            self.serial_service.write(reg.address, 0x00)

    def write_register(self, address: int, value: int):
        """
        The primary interface for the GUI to update hardware.
        1. Updates the internal cache.
        2. Transmits the packet via the serial service.
        
        :param address: Register address (0x00-0xFF)
        :param value: New value to write (0x00-0xFF)
        """
        # Update local source of truth
        self.cache[address] = value
        
        # Transmit to hardware
        # If this fails, it raises an IOError which the GUI catches to show a popup.
        self.serial_service.write(address, value)

    def get_cached_value(self, address: int) -> int:
        """
        Returns the last successfully written value for a given register.
        """
        return self.cache.get(address, 0x00)