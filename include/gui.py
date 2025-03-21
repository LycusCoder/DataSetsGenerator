from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QLabel, QLineEdit,
    QVBoxLayout, QWidget, QComboBox, QStatusBar, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont, QIcon
from include.workers import (
    LaravelWorker, ChatWorker, 
    SelfLearningWorker, CustomWorker
)

class DatasetGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Dataset Generator Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.worker = None  # Menyimpan referensi worker
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.header_label = QLabel("AI Dataset Generation System")
        self.header_label.setFont(header_font)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header_label)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)

        # Input section
        self.num_label = QLabel("Jumlah Dataset:")
        self.num_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.num_input = QLineEdit("10")
        self.num_input.setPlaceholderText("Masukkan jumlah data (1-1000)")
        form_layout.addWidget(self.num_label)
        form_layout.addWidget(self.num_input)

        self.name_label = QLabel("Nama File Output:")
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.name_input = QLineEdit("dataset")
        self.name_input.setPlaceholderText("Nama file tanpa ekstensi")
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        self.type_label = QLabel("Tipe Dataset:")
        self.type_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Laravel", "Chat", "Self-Learning", "Custom"])
        self.type_combo.setFont(QFont("Segoe UI", 10))
        self.type_combo.currentIndexChanged.connect(self.update_visibility)
        form_layout.addWidget(self.type_label)
        form_layout.addWidget(self.type_combo)

        # Topik Chat
        self.chat_topics_label = QLabel("Topik Kustom (pisahkan dengan koma):")
        self.chat_topics_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.chat_topics_label.setVisible(False)
        self.chat_topics_input = QLineEdit()
        self.chat_topics_input.setPlaceholderText("Contoh: Roleplay, Akademik, Dukungan Teknis")
        self.chat_topics_input.setVisible(False)
        form_layout.addWidget(self.chat_topics_label)
        form_layout.addWidget(self.chat_topics_input)

        # Custom Prompt
        self.custom_prompt_label = QLabel("Custom Prompt:")
        self.custom_prompt_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.custom_prompt_label.setVisible(False)
        self.custom_prompt_textedit = QTextEdit()
        self.custom_prompt_textedit.setPlaceholderText("Masukkan prompt kustom untuk dataset")
        self.custom_prompt_textedit.setVisible(False)
        form_layout.addWidget(self.custom_prompt_label)
        form_layout.addWidget(self.custom_prompt_textedit)

        main_layout.addLayout(form_layout)

        # Tombol aksi
        button_layout = QHBoxLayout()
        self.btn_generate = QPushButton("Generate Dataset")
        self.btn_generate.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate.setFixedHeight(40)
        
        self.btn_stop = QPushButton("Stop Process")
        self.btn_stop.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stop.setFixedHeight(40)
        self.btn_stop.setStyleSheet("background-color: #ff4444; color: white")
        self.btn_stop.setVisible(False)
        
        button_layout.addWidget(self.btn_generate)
        button_layout.addWidget(self.btn_stop)
        main_layout.addLayout(button_layout)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setFont(QFont("Consolas", 10))
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Siap")

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.btn_generate.clicked.connect(self.start_generation)
        self.btn_stop.clicked.connect(self.stop_generation)

    def update_visibility(self):
        dataset_type = self.type_combo.currentText()
        is_custom = dataset_type == "Custom"
        is_chat = dataset_type == "Chat"

        self.chat_topics_label.setVisible(is_chat)
        self.chat_topics_input.setVisible(is_chat)
        self.custom_prompt_label.setVisible(is_custom)
        self.custom_prompt_textedit.setVisible(is_custom)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QLabel {
                color: #E0E0E0;
                padding: 4px;
            }
            QLineEdit, QComboBox {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #6A6A6A;
            }
            QComboBox::drop-down {
                background-color: #4A4A4A;
                border-radius: 4px;
                width: 20px;
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
            QTextEdit {
                background-color: #3A3A3A;
                color: #E0E0E0;
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                padding: 10px;
            }
            QStatusBar {
                color: #C0C0C0;
                background-color: #2D2D2D;
                border-top: 1px solid #4A4A4A;
            }
        """)

    def start_generation(self):
        try:
            num = int(self.num_input.text())
            name = self.name_input.text().strip()
            dataset_type = self.type_combo.currentText()
            
            if num <= 0 or num > 1000:
                raise ValueError("Jumlah harus antara 1-1000")
                
            if dataset_type == "Custom":
                custom_prompt = self.custom_prompt_textedit.toPlainText().strip()
                if not custom_prompt:
                    raise ValueError("Prompt custom tidak boleh kosong")
                    
            self.log_area.clear()
            
            if dataset_type == "Laravel":
                self.worker = LaravelWorker(num, name)
            elif dataset_type == "Chat":
                custom_topics = self.chat_topics_input.text().strip()
                topics = [t.strip() for t in custom_topics.split(',')] if custom_topics else None
                self.worker = ChatWorker(num, name, topics=topics)
            elif dataset_type == "Self-Learning":
                self.worker = SelfLearningWorker(num, name)
            else:
                custom_prompt = self.custom_prompt_textedit.toPlainText().strip()
                self.worker = CustomWorker(num, name, custom_prompt)
                
            # Konfigurasi worker
            self.worker.log_signal.connect(self.update_log)
            self.worker.error_signal.connect(self.show_error)
            self.worker.finished.connect(self.generation_finished)
            
            # Konfigurasi tombol
            self.btn_generate.setEnabled(False)
            self.btn_stop.setVisible(True)
            self.worker.finished.connect(lambda: self.btn_stop.setVisible(False))
            self.worker.finished.connect(lambda: self.btn_generate.setEnabled(True))
            
            self.worker.start()
            self.status_bar.showMessage("Proses dimulai...")
            
        except Exception as e:
            self.show_error(str(e))

    def stop_generation(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.status_bar.showMessage("Proses dihentikan, data tersimpan!")
            self.btn_stop.setVisible(False)
            self.btn_generate.setEnabled(True)

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()

    def update_log(self, message):
        self.log_area.append(message)
        self.status_bar.showMessage("Sedang memproses...")

    def show_error(self, message):
        self.log_area.append(f"⚠️ Error: {message}")
        self.status_bar.showMessage("Error terjadi")

    def generation_finished(self):
        self.status_bar.showMessage("Proses selesai! Dataset tersimpan di folder 'datasets'")
        self.btn_stop.setVisible(False)
        self.btn_generate.setEnabled(True)