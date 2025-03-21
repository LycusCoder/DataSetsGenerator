import sys
from include.gui import DatasetGeneratorApp
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatasetGeneratorApp()
    window.show()
    sys.exit(app.exec())