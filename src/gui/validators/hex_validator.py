from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class HexValidator(QRegularExpressionValidator):
    """
    Validates that input is exactly two hexadecimal characters (0-9, A-F).
    Automatically normalizes input to uppercase.
    """

    def __init__(self, parent=None):
        # Regex: exactly two characters, restricted to hex digits.
        # We allow 0-2 characters during editing to allow typing/backspacing.
        regex = QRegularExpression(r"^[0-9A-Fa-f]{0,2}$")
        super().__init__(regex, parent)

    def validate(self, input_str: str, pos: int):
        """
        Validates the input and enforces uppercase.
        """
        # Normalize to uppercase immediately
        normalized_input = input_str.upper()
        
        state, _, new_pos = super().validate(normalized_input, pos)
        return state, normalized_input, new_pos