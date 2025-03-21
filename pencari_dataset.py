import sys
import os
import json
import requests
from difflib import SequenceMatcher
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, 
    QLabel, QLineEdit, QVBoxLayout, QWidget, QComboBox,
    QStyleFactory, QStatusBar, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QIcon

# --- Base Worker Class ---
class BaseWorker(QThread):
    finished = pyqtSignal()
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, num_entries, output_name):
        super().__init__()
        self.num_entries = num_entries
        self.output_name = output_name

    def generate_response(self, prompt, model="qwen2.5:1.5b"):
        url = "http://localhost:11434/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.9}
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")
            return None

    def is_valid_json(self, text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

# --- Laravel Dataset Worker ---
class LaravelWorker(BaseWorker):
    def run(self):
        dataset = []
        topics = [
            "routing", "controller", "Eloquent", "migration", "middleware",
            "Blade", "validation", "API resources", "event-listener", "task-scheduling"
        ]
        
        while len(dataset) < self.num_entries:
            topic = topics[len(dataset) % len(topics)]
            
            prompt = f"""
            INSTRUKSI:
            1. Buat pertanyaan UNIK tentang {topic} di Laravel untuk pemula
            2. Jawaban harus SINGKAT (max 2 kalimat) dan FOKUS pada konsep inti
            3. Berikan contoh kode yang BERBEDA dari contoh umum
            4. Format JSON wajib dengan struktur:
            
            {{
                "question": "Pertanyaan spesifik tentang {topic}",
                "answer": "Penjelasan konsep dengan bahasa sederhana",
                "code": "Contoh kode Laravel yang valid dan tidak generik",
                "source": "URL dokumentasi resmi Laravel"
            }}
            """
            
            for _ in range(3):
                response_text = self.generate_response(prompt)
                
                if response_text and self.is_valid_json(response_text):
                    entry = json.loads(response_text)
                    
                    if topic == "Blade":
                        if not any(k in entry['code'] for k in ['@extends', '@section', '@include']):
                            continue
                    
                    if all(k in entry for k in ["question", "answer", "code", "source"]) and self.is_unique(entry, dataset):
                        dataset.append(entry)
                        self.log_signal.emit(f"✅ {len(dataset)}/{self.num_entries}: {entry['question']}")
                        break
                    else:
                        self.log_signal.emit("⚠️ Duplikat atau struktur tidak lengkap")
                else:
                    self.log_signal.emit("❌ Gagal parsing JSON")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{self.output_name}_laravel_{timestamp}.json"
        output_path = os.path.join("datasets", safe_filename)
        
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
        
        self.log_signal.emit(f"\n🚀 Dataset Laravel disimpan ke {output_path}")
        self.finished.emit()

    def is_unique(self, entry, dataset, threshold=0.8):
        for existing in dataset:
            similarity = SequenceMatcher(None, entry['question'], existing['question']).ratio()
            if similarity > threshold:
                return False
        return True

# --- Chat Dataset Worker ---
class ChatWorker(BaseWorker):
    def run(self):
        dataset = []
        topics = ["Laravel", "PHP", "Database", "API", "Authentication"]
        
        while len(dataset) < self.num_entries:
            topic = topics[len(dataset) % len(topics)]
            
            prompt = f"""
            INSTRUKSI:
            1. Buat percakapan ALAMI tentang {topic}
            2. User: Pertanyaan teknis spesifik
            3. AI: Jawaban singkat dengan contoh kode jika perlu
            4. Format JSON:
            
            {{
                "user": "Pertanyaan tentang {topic}",
                "ai": "Jawaban jelas dengan kode contoh"
            }}
            """
            
            for _ in range(3):
                response = self.generate_response(prompt)
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    if all(k in entry for k in ["user", "ai"]) and self.is_unique(entry, dataset):
                        dataset.append(entry)
                        self.log_signal.emit(f"✅ {len(dataset)}/{self.num_entries}: {entry['user']}")
                        break
            
        self.save_dataset(dataset, "chat")

    def is_unique(self, entry, dataset, threshold=0.8):
        for existing in dataset:
            similarity = SequenceMatcher(None, entry['user'], existing['user']).ratio()
            if similarity > threshold:
                return False
        return True

    def save_dataset(self, dataset, type_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_name}_{type_name}_{timestamp}.json"
        output_path = os.path.join("datasets", filename)
        
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
            
        self.log_signal.emit(f"\n🚀 Dataset {type_name} disimpan ke {output_path}")
        self.finished.emit()

# --- Self Learning Dataset Worker ---
class SelfLearningWorker(BaseWorker):
    def run(self):
        dataset = []
        topics = ["Advanced Eloquent", "Microservices", "Queue Workers", "Server Optimization", "Package Development"]
        
        while len(dataset) < self.num_entries:
            topic = topics[len(dataset) % len(topics)]
            
            prompt = f"""
            INSTRUKSI:
            1. Buat pertanyaan KOMPLEKS tentang {topic} yang jarang dibahas
            2. Pertanyaan harus spesifik dan membutuhkan penjelasan mendalam
            3. Format JSON:
            
            {{
                "question": "Pertanyaan teknis kompleks tentang {topic}",
                "status": "pending",
                "learned_at": null
            }}
            """
            
            for _ in range(3):
                response = self.generate_response(prompt)
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    if all(k in entry for k in ["question", "status", "learned_at"]):
                        dataset.append(entry)
                        self.log_signal.emit(f"✅ {len(dataset)}/{self.num_entries}: {entry['question']}")
                        break
            
        self.save_dataset(dataset, "self_learning")

    def save_dataset(self, dataset, type_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_name}_{type_name}_{timestamp}.json"
        output_path = os.path.join("datasets", filename)
        
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
            
        self.log_signal.emit(f"\n🚀 Dataset {type_name} disimpan ke {output_path}")
        self.finished.emit()

# --- Custom Dataset Worker ---
class CustomWorker(BaseWorker):
    def __init__(self, num_entries, output_name, custom_prompt):
        super().__init__(num_entries, output_name)
        self.custom_prompt = custom_prompt

    def run(self):
        dataset = []
        
        while len(dataset) < self.num_entries:
            prompt = f"""
            {self.custom_prompt.strip()}
            
            Format JSON wajib:
            {{
                "question": "Pertanyaan sesuai instruksi",
                "answer": "Jawaban sesuai instruksi",
                "code": "Contoh kode jika diperlukan",
                "source": "Sumber referensi jika ada"
            }}
            """
            
            for _ in range(3):
                response = self.generate_response(prompt)
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    if all(k in entry for k in ["question", "answer"]) and self.is_unique(entry, dataset):
                        dataset.append(entry)
                        self.log_signal.emit(f"✅ {len(dataset)}/{self.num_entries}: {entry['question']}")
                        break
            
        self.save_dataset(dataset, "custom")

    def is_unique(self, entry, dataset, threshold=0.8):
        for existing in dataset:
            similarity = SequenceMatcher(None, entry['question'], existing['question']).ratio()
            if similarity > threshold:
                return False
        return True

    def save_dataset(self, dataset, type_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_name}_{type_name}_{timestamp}.json"
        output_path = os.path.join("datasets", filename)
        
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
            
        self.log_signal.emit(f"\n🚀 Dataset custom disimpan ke {output_path}")
        self.finished.emit()

# --- GUI Utama ---
class DatasetGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Dataset Generator Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/logo.ico"))  # Logo kustom
        
        # Inisialisasi UI
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        # Layout Utama
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header Section
        header_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.header_label = QLabel("AI Dataset Generation System")
        self.header_label.setFont(header_font)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header_label)

        # Form Section
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)
        
        # Input Jumlah Data
        self.num_label = QLabel("Jumlah Dataset:")
        self.num_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.num_input = QLineEdit("10")
        self.num_input.setPlaceholderText("Masukkan jumlah data (1-1000)")
        form_layout.addWidget(self.num_label)
        form_layout.addWidget(self.num_input)
        
        # Input Nama File
        self.name_label = QLabel("Nama File Output:")
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.name_input = QLineEdit("dataset")
        self.name_input.setPlaceholderText("Nama file tanpa ekstensi")
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)
        
        # Pilihan Tipe Dataset
        self.type_label = QLabel("Tipe Dataset:")
        self.type_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Laravel", "Chat", "Self-Learning", "Custom"])
        self.type_combo.setFont(QFont("Segoe UI", 10))
        self.type_combo.currentIndexChanged.connect(self.toggle_custom_prompt)
        form_layout.addWidget(self.type_label)
        form_layout.addWidget(self.type_combo)
        
        # Custom Prompt Section
        self.custom_prompt_label = QLabel("Custom Prompt:")
        self.custom_prompt_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.custom_prompt_label.setVisible(False)
        self.custom_prompt_textedit = QTextEdit()
        self.custom_prompt_textedit.setPlaceholderText("Masukkan prompt kustom untuk dataset")
        self.custom_prompt_textedit.setVisible(False)
        form_layout.addWidget(self.custom_prompt_label)
        form_layout.addWidget(self.custom_prompt_textedit)
        
        main_layout.addLayout(form_layout)
        
        # Tombol Generate
        self.btn_generate = QPushButton("Generate Dataset")
        self.btn_generate.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate.setFixedHeight(40)
        main_layout.addWidget(self.btn_generate)
        
        # Area Log
        self.log_area = QTextEdit()
        self.log_area.setFont(QFont("Consolas", 10))
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Siap")
        
        # Container Widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Connections
        self.btn_generate.clicked.connect(self.start_generation)

    def toggle_custom_prompt(self):
        is_custom = self.type_combo.currentText() == "Custom"
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
            self.status_bar.showMessage("Proses dimulai...")
            
            if dataset_type == "Laravel":
                self.worker = LaravelWorker(num, name)
            elif dataset_type == "Chat":
                self.worker = ChatWorker(num, name)
            elif dataset_type == "Self-Learning":
                self.worker = SelfLearningWorker(num, name)
            else:
                self.worker = CustomWorker(num, name, custom_prompt)
                
            self.worker.log_signal.connect(self.update_log)
            self.worker.error_signal.connect(self.show_error)
            self.worker.finished.connect(self.generation_finished)
            self.worker.start()
            
        except Exception as e:
            self.show_error(str(e))

    def update_log(self, message):
        self.log_area.append(message)
        self.status_bar.showMessage("Sedang memproses...")
        
    def show_error(self, message):
        self.log_area.append(f"❌ Error: {message}")
        self.status_bar.showMessage("Error terjadi")
        
    def generation_finished(self):
        self.status_bar.showMessage("Proses selesai! Dataset tersimpan di folder 'datasets'")

if __name__ == "__main__":
    os.makedirs("datasets", exist_ok=True)
    
    app = QApplication(sys.argv)
    window = DatasetGeneratorApp()
    window.show()
    sys.exit(app.exec())