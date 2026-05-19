from src.models.register import RegisterDefinition

# UART Settings
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
SYNC_BYTE = 0x77

# Mock Mode Toggle
MOCK_MODE = True  # Set to False for production hardware

# Register Groups
GROUP_VOICE_1 = "Voice 1"
GROUP_VOICE_2 = "Voice 2"
GROUP_VOICE_3 = "Voice 3"
GROUP_FILTER_MASTER = "Filter / Master"

# Complete Register List
REGISTERS = [
    # Voice 1
    RegisterDefinition(0x00, "FREQLO1", "Voice 1 frequency low byte", GROUP_VOICE_1),
    RegisterDefinition(0x01, "FREQHI1", "Voice 1 frequency high byte", GROUP_VOICE_1),
    RegisterDefinition(0x02, "PWLO1", "Voice 1 pulse width low byte", GROUP_VOICE_1),
    RegisterDefinition(0x03, "PWHI1", "Voice 1 pulse width high nibble", GROUP_VOICE_1),
    RegisterDefinition(0x04, "CTRL1", "Voice 1 waveform and control", GROUP_VOICE_1),
    RegisterDefinition(0x05, "AD1", "Voice 1 ADSR attack and decay", GROUP_VOICE_1),
    RegisterDefinition(0x06, "SR1", "Voice 1 ADSR sustain and release", GROUP_VOICE_1),

    # Voice 2
    RegisterDefinition(0x07, "FREQLO2", "Voice 2 frequency low byte", GROUP_VOICE_2),
    RegisterDefinition(0x08, "FREQHI2", "Voice 2 frequency high byte", GROUP_VOICE_2),
    RegisterDefinition(0x09, "PWLO2", "Voice 2 pulse width low byte", GROUP_VOICE_2),
    RegisterDefinition(0x0A, "PWHI2", "Voice 2 pulse width high nibble", GROUP_VOICE_2),
    RegisterDefinition(0x0B, "CTRL2", "Voice 2 waveform and control", GROUP_VOICE_2),
    RegisterDefinition(0x0C, "AD2", "Voice 2 ADSR attack and decay", GROUP_VOICE_2),
    RegisterDefinition(0x0D, "SR2", "Voice 2 ADSR sustain and release", GROUP_VOICE_2),

    # Voice 3
    RegisterDefinition(0x0E, "FREQLO3", "Voice 3 frequency low byte", GROUP_VOICE_3),
    RegisterDefinition(0x0F, "FREQHI3", "Voice 3 frequency high byte", GROUP_VOICE_3),
    RegisterDefinition(0x10, "PWLO3", "Voice 3 pulse width low byte", GROUP_VOICE_3),
    RegisterDefinition(0x11, "PWHI3", "Voice 3 pulse width high nibble", GROUP_VOICE_3),
    RegisterDefinition(0x12, "CTRL3", "Voice 3 waveform and control", GROUP_VOICE_3),
    RegisterDefinition(0x13, "AD3", "Voice 3 ADSR attack and decay", GROUP_VOICE_3),
    RegisterDefinition(0x14, "SR3", "Voice 3 ADSR sustain and release", GROUP_VOICE_3),

    # Filter / Master
    RegisterDefinition(0x15, "FCLO", "Filter cutoff low bits", GROUP_FILTER_MASTER),
    RegisterDefinition(0x16, "FCHI", "Filter cutoff high bits", GROUP_FILTER_MASTER),
    RegisterDefinition(0x17, "RESFILT", "Filter resonance and routing", GROUP_FILTER_MASTER),
    RegisterDefinition(0x18, "MODEVOL", "Filter mode and master volume", GROUP_FILTER_MASTER),
]