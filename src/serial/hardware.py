import serial
from src.serial.base import SerialServiceBase
from src.config import settings

class HardwareSerialService(SerialServiceBase):
    """
    Concrete implementation of SerialServiceBase using pySerial for real hardware communication.
    """

    def __init__(self):
        """
        Attempts to initialize and open the serial port defined in settings.
        Raises ConnectionError if the port cannot be opened.
        """
        try:
            self._ser = serial.Serial(
                port=settings.SERIAL_PORT,
                baudrate=settings.BAUD_RATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1  # Short timeout for writes
            )
        except Exception as e:
            # Re-raise as a generic ConnectionError for the Controller to catch and display in a popup
            raise ConnectionError(f"Could not open serial port {settings.SERIAL_PORT}: {str(e)}")

    def write(self, address: int, data: int) -> None:
        """
        Constructs and sends the 3-byte packet [SYNC][ADDR][DATA].
        """
        try:
            # Construct the packet as a bytes object
            packet = bytes([settings.SYNC_BYTE, address & 0xFF, data & 0xFF])
            
            self._ser.write(packet)
            self._ser.flush()  # Ensure data is actually sent out of the OS buffer
            
        except Exception as e:
            # Re-raise as an IOError for the Controller to handle runtime failure popups
            raise IOError(f"Failed to transmit to hardware: {str(e)}")