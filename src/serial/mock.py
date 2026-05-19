from src.serial.base import SerialServiceBase
from src.config import settings

class MockSerialService(SerialServiceBase):
    """
    Concrete implementation of SerialServiceBase that simulates serial communication.
    Useful for GUI development and logic testing without physical hardware.
    """

    def write(self, address: int, data: int) -> None:
        """
        Simulates transmission by printing the packet details to the console.
        """
        packet_str = f"0x{settings.SYNC_BYTE:02X} 0x{address:02X} 0x{data:02X}"
        print(f"[MOCK UART] Writing Packet: [{packet_str}]")