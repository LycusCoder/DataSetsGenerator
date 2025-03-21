```markdown
# 🚀 AI Dataset Generator Pro 🤖

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue) 
![PyQt6](https://img.shields.io/badge/PyQt6-6.5.1-green) 
![License](https://img.shields.io/badge/License-MIT-red)

![AI Dataset Generator Pro](assets/logo.ico)

**AI Dataset Generator Pro** adalah alat profesional untuk membuat dataset terstruktur dengan kecerdasan buatan. Dibangun dengan Python dan PyQt6, aplikasi ini membantu pengembang, peneliti, dan data scientist menghasilkan dataset berkualitas tinggi secara efisien.

## 🌟 Fitur Utama
| Fitur                | Deskripsi                                                                 |
|----------------------|---------------------------------------------------------------------------|
| **AI-Powered**       | Menggunakan model seperti `qwen2.5:1.5b` untuk generasi data otomatis     |
| **Multi-Template**   | 4+ template dataset: Laravel, Chat, Self-Learning, dan Custom            |
| **Deduplikasi Cerdas** | Utilitas `deduplicateworker.py` untuk eliminasi data duplikat           |
| **Antarmuka Modern** | GUI berbasis PyQt6 dengan progress tracking real-time                   |
| **Validasi Ketat**   | Pemeriksaan JSON, validasi kode, dan sistem threshold similarity         |

## 📦 Komponen Proyek
```bash
.
├── 🖥️ GUI                  # File antarmuka PyQt6
├── 🧠 Workers              # Mesin generasi dataset
├── 🔄 deduplicateworker.py # Utilitas deduplikasi JSON
├── 📂 datasets             # Folder penyimpanan hasil
└── 🛠️ utils.py             # Fungsi bantu teknis
```

## 🔧 Persyaratan Teknis
- Python 3.8+
- PyQt6 (`pip install PyQt6`)
- Requests (`pip install requests`)
- Server Ollama berjalan di `http://localhost:11434`

## 🚀 Cara Menggunakan

### 1. Generasi Dataset
```bash
python pencari_dataset.py
```
![GUI Demo](assets/gui_screenshot.png)

### 2. Deduplikasi Dataset
```bash
python deduplicateworker.py input.json output.json --threshold 0.8
```

## 🔍 Template Dataset
### 1. Laravel Dataset
```json
{
  "question": "Bagaimana membuat middleware custom?",
  "answer": "Gunakan php artisan make:middleware ...",
  "code": "<?php namespace App\\Http\\Middleware...",
  "source": "https://laravel.com/docs/middleware"
}
```

### 2. Chat Dataset
```json
{
  "scenario": "Developer junior bertanya tentang autentikasi",
  "user": "Bagaimana implementasi JWT di Laravel?",
  "ai": "1. Install package jwt-auth...\n2. Konfigurasi auth.php...",
  "follow_up": "Bagaimana refresh token?",
  "resources": ["https://jwt.io"]
}
```

## 🛠️ Utilitas Profesional
### Deduplikasi JSON
```python
# Contoh penggunaan:
python deduplicateworker.py datasets/input.json datasets/output.json --threshold 0.85
```
- Menggunakan algoritma SequenceMatcher
- Threshold similarity 0.0 (semua unik) - 1.0 (identik)
- Support file besar (>1GB)

## 📚 Dokumentasi Lengkap
Kunjungi [Wiki Proyek](https://github.com/LycusCoder/DataSetsGenerator/wiki) untuk:
- Panduan instalasi server Ollama
- Konfigurasi model AI
- Contoh dataset
- Best practices

## 🤝 Kontribusi
1. Fork repositori
2. Buat branch (`git checkout -b feature-xyz`)
3. Commit perubahan (`git commit -m 'Add feature xyz'`)
4. Push ke branch (`git push origin feature-xyz`)
5. Buat Pull Request

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE)
```
