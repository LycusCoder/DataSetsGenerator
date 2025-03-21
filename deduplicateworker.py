import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit,
    QLabel, QLineEdit, QVBoxLayout, QWidget, QFileDialog,
    QProgressBar, QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon

class DeduplicateWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            self.log.emit("Membaca data dari file JSON...")
            with open(self.input_path, 'r') as file:
                data = json.load(file)

            unique_items = {}
            total = len(data)
            
            for i, item in enumerate(data, 1):
                key = (item['question'], item['answer'], item['code'], item['source'])
                unique_items[key] = item
                self.progress.emit(int(i/total * 100))
                
            unique_data = list(unique_items.values())
            
            with open(self.output_path, 'w') as file:
                json.dump(unique_data, file, indent=4)
                
            self.log.emit(f"Proses selesai! {len(unique_data)}/{len(data)} item unik")
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))

class DeduplicatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Deduplicator Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.header = QLabel("JSON Deduplication Tool")
        self.header.setFont(header_font)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header)

        # Input section
        input_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Pilih file JSON...")
        self.browse_btn = QPushButton("...")
        self.browse_btn.setFixedWidth(30)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.browse_btn)
        main_layout.addLayout(input_layout)

        # Output section
        self.output_path = QLineEdit("datasets/laravel_dataset_unique.json")
        self.output_path.setPlaceholderText("Nama file output...")
        main_layout.addWidget(self.output_path)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        main_layout.addWidget(self.progress)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        # Process button
        self.process_btn = QPushButton("Proses Deduplikasi")
        self.process_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.process_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(self.process_btn)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.browse_btn.clicked.connect(self.select_input)
        self.process_btn.clicked.connect(self.start_processing)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QLabel {
                color: #E0E0E0;
                padding: 4px;
            }
            QLineEdit {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #6A6A6A;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QProgressBar {
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 0.5px;
            }
            QTextEdit {
                background-color: #3A3A3A;
                color: #E0E0E0;
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                padding: 10px;
            }
        """)

    def select_input(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File JSON",
            "",
            "JSON Files (*.json)"
        )
        if path:
            self.input_path.setText(path)

    def start_processing(self):
        input_path = self.input_path.text().strip()
        output_path = self.output_path.text().strip()

        if not os.path.exists(input_path):
            self.log_area.append("⚠️ File input tidak valid")
            return

        self.worker = DeduplicateWorker(input_path, output_path)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.log_area.append)
        self.worker.error.connect(lambda e: self.log_area.append(f"⚠️ Error: {e}"))
        self.worker.finished.connect(lambda: self.progress.setValue(100))
        self.worker.start()
        self.process_btn.setEnabled(False)
        self.worker.finished.connect(lambda: self.process_btn.setEnabled(True))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeduplicatorApp()
    window.show()
    sys.exit(app.exec())