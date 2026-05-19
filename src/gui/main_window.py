from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QGroupBox, QApplication
)
from PyQt6.QtCore import Qt
from src.config import settings
from src.gui.widgets.register_row import RegisterRow
from src.controller.app_controller import AppController

class MainWindow(QMainWindow):
    """
    The main application window, responsible for laying out the GUI elements.
    It creates the scrollable area, groups registers, and instantiates RegisterRow widgets.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("SID Chip Register Controller")
        self.setGeometry(100, 100, 1400, 1000) # Spec 12.2

        self._init_ui()

    def _init_ui(self):
        # Central widget to hold the scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Scroll Area (Spec 12.2)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll_area)

        # Widget inside the scroll area to hold the grouped registers
        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)
        self.scroll_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align content to top

        self._create_register_groups()

    def _create_register_groups(self):
        # Group registers by their 'group' attribute
        grouped_registers = {}
        for reg_def in settings.REGISTERS:
            if reg_def.group not in grouped_registers:
                grouped_registers[reg_def.group] = []
            grouped_registers[reg_def.group].append(reg_def)

        # Create a QGroupBox for each group (Spec 12.3)
        for group_name in [settings.GROUP_VOICE_1, settings.GROUP_VOICE_2, 
                           settings.GROUP_VOICE_3, settings.GROUP_FILTER_MASTER]:
            
            if group_name not in grouped_registers:
                continue # Skip if a group has no registers defined

            group_box = QGroupBox(group_name)
            group_layout = QVBoxLayout(group_box)
            group_layout.setContentsMargins(10, 20, 10, 10) # Adjust margins for title
            group_layout.setSpacing(5)

            # Add RegisterRow widgets to the group
            for reg_def in grouped_registers[group_name]:
                register_row = RegisterRow(reg_def, self.controller)
                group_layout.addWidget(register_row)
            
            # Add a stretch to push rows to the top within the group
            group_layout.addStretch(1)
            self.scroll_layout.addWidget(group_box)

        self.scroll_layout.addStretch(1) # Push all groups to the top of the scroll area
