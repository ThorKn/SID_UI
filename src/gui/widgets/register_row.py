from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from src.models.register import RegisterDefinition
from src.gui.validators.hex_validator import HexValidator

class RegisterRow(QWidget):
    """
    A reusable widget representing a single hardware register row.
    Implements the layout and interaction logic defined in Specs 14, 16, and 17.
    """

    def __init__(self, definition: RegisterDefinition, controller, parent=None):
        super().__init__(parent)
        self.definition = definition
        self.controller = controller

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(20)

        # Column 1: Register Name (Spec 14)
        self.name_label = QLabel(self.definition.name)
        self.name_label.setMinimumWidth(120)
        self.name_label.setToolTip(self.definition.description)
        layout.addWidget(self.name_label)

        # Column 2: Address (Spec 15: Uppercase, 2-digit, 0x prefix)
        addr_text = f"0x{self.definition.address:02X}"
        self.addr_label = QLabel(addr_text)
        self.addr_label.setMinimumWidth(60)
        self.addr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.addr_label)

        # Column 3: Current Value (Spec 18: Last successful write)
        current_val = self.controller.get_cached_value(self.definition.address)
        self.current_val_label = QLabel(f"0x{current_val:02X}")
        self.current_val_label.setMinimumWidth(80)
        self.current_val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_val_label)

        # Column 4: New Value Input (Spec 16: Two hex digits, no prefix)
        self.input_field = QLineEdit()
        self.input_field.setFixedWidth(60)
        self.input_field.setPlaceholderText("00")
        self.input_field.setValidator(HexValidator(self))
        self.input_field.returnPressed.connect(self.handle_write)
        layout.addWidget(self.input_field)

        # Column 5: Action Button
        self.write_button = QPushButton("WRITE")
        self.write_button.setFixedWidth(100)
        self.write_button.clicked.connect(self.handle_write)
        layout.addWidget(self.write_button)

    def handle_write(self):
        """Workflow defined in Spec 17."""
        text = self.input_field.text()

        # Spec 16: Exactly two hexadecimal digits
        if len(text) != 2:
            QMessageBox.warning(self, "Invalid Input", 
                                f"Register {self.definition.name} requires exactly two hexadecimal digits (e.g., '00' or 'FF').")
            return

        try:
            value = int(text, 16)
            self.controller.write_register(self.definition.address, value)
            
            # Update GUI on success (Spec 17.7)
            self.current_val_label.setText(f"0x{value:02X}")
            
        except IOError as e:
            # Spec 6.3: Runtime failure handling
            QMessageBox.critical(self, "Transmission Error", 
                                 f"Failed to communicate with hardware:\n{str(e)}\n\nPlease restart the application.")