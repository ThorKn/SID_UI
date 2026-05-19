import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from src.gui.main_window import MainWindow
from src.controller.app_controller import AppController
from src.config import settings

def main():
    app = QApplication(sys.argv)

    # Apply the QSS stylesheet (Spec 12.1)
    try:
        with open("src/gui/styles/theme.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", "Theme stylesheet 'theme.qss' not found.")
        sys.exit(1)

    controller = None
    try:
        # Initialize the Application Controller, which also attempts to open the serial port
        controller = AppController()
    except ConnectionError as e:
        # Handle startup failure (Spec 6.2)
        QMessageBox.critical(None, "Connection Error", 
                             f"Failed to connect to serial port:\n{str(e)}\n\n"
                             "Please ensure the device is connected and permissions are correct.")
        sys.exit(1) # Terminate application immediately

    # If controller initialized successfully, proceed with GUI
    main_window = MainWindow(controller)
    main_window.show()

    # Perform initial hardware sync (Spec 6.1)
    controller.startup_sync()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
