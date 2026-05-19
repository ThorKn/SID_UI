from abc import ABC, abstractmethod

class SerialServiceBase(ABC):
    """
    Abstract Base Class defining the interface for serial communication services.
    This ensures that both hardware and mock implementations adhere to the same contract.
    """

    @abstractmethod
    def write(self, address: int, data: int) -> None:
        """
        Transmits a 3-byte packet: [SYNC_BYTE][address][data] to the serial device.
        The SYNC_BYTE is handled internally by the concrete implementation.
        
        :param address: The one-byte register address (0x00 - 0xFF).
        :param data: The one-byte data value to write (0x00 - 0xFF).
        """
        pass