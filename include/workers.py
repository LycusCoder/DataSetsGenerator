import os
import json
import requests
from difflib import SequenceMatcher
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal

class BaseWorker(QThread):
    finished = pyqtSignal()
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()  # Pindahkan ke class attribute

    def __init__(self, num_entries, output_name):
        super().__init__()
        self.num_entries = num_entries
        self.output_name = output_name
        self._is_running = True
        self.dataset = []  # Inisialisasi dataset di sini
        self.stop_signal.connect(self.stop)

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
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            self.log_signal.emit(f"⚠️ Connection error: {str(e)}")
        except json.JSONDecodeError:
            self.log_signal.emit("⚠️ Invalid JSON response")
        except Exception as e:
            self.log_signal.emit(f"⚠️ Unexpected error: {str(e)}")
        return None

    def is_valid_json(self, text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    def stop(self):
        self._is_running = False
        self.log_signal.emit("⚠️ Proses dihentikan, menyimpan data...")
        if self.dataset:
            self.save_dataset(self.dataset, self.dataset_type)
        self.finished.emit()

    def run(self):
        self.dataset_type = "default"
        try:
            while self._is_running and len(self.dataset) < self.num_entries:
                # Logika pembuatan dataset (diimplementasikan di subclass)
                pass
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            if self.dataset and self._is_running:  # Hanya simpan jika tidak dihentikan paksa
                self.save_dataset(self.dataset, self.dataset_type)
                self.finished.emit()

    def save_dataset(self, dataset, type_name):
        os.makedirs("datasets", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_name}_{type_name}_{timestamp}.json"
        output_path = os.path.join("datasets", filename)
        
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
            
        self.log_signal.emit(f"\n🚀 Dataset {type_name} disimpan ke {output_path}")

class LaravelWorker(BaseWorker):
    def run(self):
        self.dataset_type = "laravel"
        topics = [
            "routing", "controller", "Eloquent", "migration", "middleware",
            "Blade", "validation", "API resources", "event-listener", "task-scheduling"
        ]
        
        while len(self.dataset) < self.num_entries and self._is_running:
            topic = topics[len(self.dataset) % len(topics)]
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
                if not self._is_running:
                    break
                    
                response_text = self.generate_response(prompt)
                
                if response_text and self.is_valid_json(response_text):
                    entry = json.loads(response_text)
                    
                    # Validasi struktur
                    required_fields = ["question", "answer", "code", "source"]
                    if not all(k in entry for k in required_fields):
                        self.log_signal.emit("⚠️ Struktur data tidak lengkap")
                        continue
                        
                    if not isinstance(entry['code'], str) or not entry['code'].strip():
                        self.log_signal.emit("⚠️ Code field kosong atau tidak valid")
                        continue
                        
                    if topic == "Blade":
                        if not any(k in entry['code'] for k in ['@extends', '@section', '@include']):
                            self.log_signal.emit("⚠️ Kode Blade tidak mengandung directive wajib")
                            continue
                            
                    if self.is_unique(entry, self.dataset):
                        self.dataset.append(entry)
                        self.log_signal.emit(f"✓ {len(self.dataset)}/{self.num_entries}: {entry['question']}")
                        break
                    else:
                        self.log_signal.emit("⚠️ Duplikat atau struktur tidak lengkap")
                else:
                    self.log_signal.emit("⚠️ Gagal parsing JSON")

    def is_unique(self, entry, dataset, threshold=0.8):
        for existing in dataset:
            similarity = SequenceMatcher(None, entry['question'], existing['question']).ratio()
            if similarity > threshold:
                return False
        return True

class ChatWorker(BaseWorker):
    def __init__(self, num_entries, output_name, topics=None, 
                 personas=None, include_followup=True):
        super().__init__(num_entries, output_name)
        self.topics = topics or ["Laravel", "PHP", "Database", "API", "Authentication"]
        self.personas = personas or [
            "Senior Developer",
            "Technical Consultant",
            "Community Moderator",
            "Code Mentor"
        ]
        self.include_followup = include_followup

    def run(self):
        self.dataset_type = "chat"
        while len(self.dataset) < self.num_entries and self._is_running:
            topic = self.topics[len(self.dataset) % len(self.topics)]
            persona = self.personas[len(self.dataset) % len(self.personas)]
            
            prompt = f"""
            🎭 ROLEPLAY SCENARIO 🎭
            Anda adalah {persona} dengan kepribadian:
            - Ramah dan sabar
            - Suka memberikan analogi kehidupan nyata
            - Menambahkan emoji untuk ekspresi
            - Menanyakan follow-up questions
            
            📝 INSTRUKSI:
            1. Buat percakapan INTERAKTIF tentang {topic}
            2. User: Pertanyaan teknis KOMPLEKS dengan konteks nyata
            3. AI: 
               - Jawaban LANGKAH-DEMI-LANGKAH
               - Contoh kode PRAKTIS
               - Tips pro
               - Pertanyaan lanjutan untuk eksplorasi
               - Sumber referensi
            
            📊 FORMAT JSON WAJIB:
            {{
                "scenario": "Deskripsi situasi roleplay",
                "user": "Pertanyaan dengan konteks spesifik",
                "ai": "Jawaban terstruktur dengan kode",
                "follow_up": "Pertanyaan lanjutan (opsional)",
                "resources": ["URL1", "URL2"]
            }}
            """
            
            for _ in range(3):
                if not self._is_running:
                    break
                    
                response = self.generate_response(prompt, model="qwen2.5:7b")
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    
                    # Validasi struktur yang lebih ketat
                    required_fields = ["scenario", "user", "ai"]
                    if not all(k in entry for k in required_fields):
                        self.log_signal.emit("⚠️ Struktur data tidak lengkap")
                        continue
                        
                    # Validasi kualitas konten
                    if len(entry['ai']) < 200 or "```" not in entry['ai']:
                        self.log_signal.emit("⚠️ Jawaban terlalu singkat atau tanpa contoh kode")
                        continue
                        
                    if self.is_unique(entry, self.dataset):
                        self.dataset.append(entry)
                        self.log_signal.emit(
                            f"✓ {len(self.dataset)}/{self.num_entries}: "
                            f"[{persona}] {entry['user'][:50]}..."
                        )
                        break
                else:
                    self.log_signal.emit("⚠️ Gagal parsing JSON")

    def is_unique(self, entry, dataset, threshold=0.7):
        for existing in dataset:
            # Cek similaritas pertanyaan dan skenario
            similarity = max(
                SequenceMatcher(None, entry['user'], existing['user']).ratio(),
                SequenceMatcher(None, entry['scenario'], existing['scenario']).ratio()
            )
            if similarity > threshold:
                return False
        return True

class SelfLearningWorker(BaseWorker):
    def run(self):
        self.dataset_type = "self_learning"
        topics = ["Advanced Eloquent", "Microservices", "Queue Workers", "Server Optimization", "Package Development"]
        
        while len(self.dataset) < self.num_entries and self._is_running:
            topic = topics[len(self.dataset) % len(topics)]
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
                if not self._is_running:
                    break
                    
                response = self.generate_response(prompt)
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    if all(k in entry for k in ["question", "status", "learned_at"]):
                        self.dataset.append(entry)
                        self.log_signal.emit(f"✓ {len(self.dataset)}/{self.num_entries}: {entry['question']}")
                        break

class CustomWorker(BaseWorker):
    def __init__(self, num_entries, output_name, custom_prompt):
        super().__init__(num_entries, output_name)
        self.custom_prompt = custom_prompt

    def run(self):
        self.dataset_type = "custom"
        while len(self.dataset) < self.num_entries and self._is_running:
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
                if not self._is_running:
                    break
                    
                response = self.generate_response(prompt)
                if response and self.is_valid_json(response):
                    entry = json.loads(response)
                    required_fields = ["question", "answer"]
                    if all(k in entry for k in required_fields) and self.is_unique(entry, self.dataset):
                        self.dataset.append(entry)
                        self.log_signal.emit(f"✓ {len(self.dataset)}/{self.num_entries}: {entry['question']}")
                        break

    def is_unique(self, entry, dataset, threshold=0.8):
        for existing in dataset:
            similarity = SequenceMatcher(None, entry['question'], existing['question']).ratio()
            if similarity > threshold:
                return False
        return True