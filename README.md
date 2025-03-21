Berikut adalah contoh **README.md** yang sesuai dengan kode Anda. README ini memberikan penjelasan yang jelas tentang proyek, fitur-fiturnya, cara menginstal dependensi, dan cara menjalankan aplikasi.

---

# AI Dataset Generator Pro

![Logo](assets/logo.ico)

**AI Dataset Generator Pro** adalah aplikasi berbasis Python yang dirancang untuk membantu pengguna dalam menghasilkan dataset secara otomatis atau semi-otomatis menggunakan model AI seperti `qwen2.5:1.5b`. Aplikasi ini menyediakan utilitas untuk membuat dataset terstruktur dalam format JSON untuk berbagai kebutuhan, seperti pembelajaran mesin, dokumentasi, atau analisis data.

## Fitur Utama
- **Pembuatan Dataset Otomatis**: Menggunakan API AI untuk menghasilkan dataset berdasarkan instruksi yang diberikan.
- **Berbagai Tipe Dataset**: Mendukung pembuatan dataset untuk topik seperti Laravel, Chat, Self-Learning, dan Custom Prompt.
- **Antarmuka Grafis (GUI)**: Dilengkapi dengan antarmuka berbasis PyQt6 untuk kemudahan penggunaan.
- **Penghapusan Duplikat Otomatis**: Memastikan bahwa dataset yang dihasilkan unik dan tidak mengandung duplikat.
- **Penyimpanan Terstruktur**: Dataset disimpan dalam format JSON dengan struktur yang terorganisasi.

## Tipe Dataset yang Didukung
1. **Laravel Dataset**:
   - Topik: Routing, Controller, Eloquent, Migration, Middleware, Blade, Validation, API Resources, Event-Listener, Task-Scheduling.
   - Format: JSON dengan pertanyaan, jawaban, contoh kode, dan sumber referensi.

2. **Chat Dataset**:
   - Topik: Laravel, PHP, Database, API, Authentication.
   - Format: JSON dengan percakapan alami antara user dan AI.

3. **Self-Learning Dataset**:
   - Topik: Advanced Eloquent, Microservices, Queue Workers, Server Optimization, Package Development.
   - Format: JSON dengan pertanyaan kompleks dan status pembelajaran.

4. **Custom Dataset**:
   - Fleksibel untuk kebutuhan khusus dengan prompt yang dapat disesuaikan oleh pengguna.

## Persyaratan Sistem
- **Python 3.8+**
- **Dependencies**: Lihat file `requirements.txt` untuk daftar package yang diperlukan.
- **API Lokal**: Aplikasi memerlukan server lokal yang berjalan di `http://localhost:11434/api/generate`.

## Instalasi
1. **Clone Repositori**:
   ```bash
   git clone https://github.com/LycusCoder/DataSetsGenerator.git
   cd DataSetsGenerator
   ```

2. **Instal Dependensi**:
   Pastikan Anda sudah memiliki `pip` dan `venv` terinstal. Kemudian jalankan:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**:
   ```bash
   python pencari_dataset.py
   ```

## Cara Menggunakan
1. **Buka Aplikasi**:
   Jalankan aplikasi melalui GUI dengan perintah:
   ```bash
   python pencari_dataset.py
   ```

2. **Isi Formulir**:
   - Masukkan jumlah dataset yang ingin dihasilkan.
   - Tentukan nama file output.
   - Pilih tipe dataset dari dropdown (`Laravel`, `Chat`, `Self-Learning`, atau `Custom`).
   - Jika memilih `Custom`, masukkan prompt kustom di area teks yang tersedia.

3. **Klik Tombol "Generate Dataset"**:
   Aplikasi akan mulai menghasilkan dataset berdasarkan parameter yang dimasukkan. Proses ini mungkin memerlukan waktu tergantung pada jumlah dataset dan respons API.

4. **Cek Hasil**:
   Dataset yang dihasilkan akan disimpan dalam folder `datasets` dengan format:
   ```
   {output_name}_{type}_{timestamp}.json
   ```

## Struktur File Output
Contoh struktur JSON untuk dataset:
```json
[
    {
        "question": "Pertanyaan spesifik tentang topik tertentu",
        "answer": "Penjelasan singkat dengan bahasa sederhana",
        "code": "Contoh kode yang valid",
        "source": "URL sumber referensi"
    },
    ...
]
```

## Kontribusi
Kontribusi sangat diterima! Silakan fork repositori ini, buat branch baru, dan ajukan pull request untuk perubahan atau fitur baru.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

### FAQ
**Q: Apakah saya memerlukan server API lokal?**  
A: Ya, aplikasi ini memerlukan server API lokal yang berjalan di `http://localhost:11434/api/generate`. Pastikan server sudah aktif sebelum menjalankan aplikasi.

**Q: Bagaimana cara menambahkan topik baru?**  
A: Anda dapat memodifikasi daftar topik dalam kode atau menggunakan opsi `Custom` untuk menambahkan prompt kustom.

**Q: Apakah dataset yang dihasilkan unik?**  
A: Ya, aplikasi menggunakan algoritma pemeriksaan kesamaan untuk memastikan dataset yang dihasilkan unik.

---

Dengan README ini, pengguna akan lebih mudah memahami cara menggunakan aplikasi Anda dan bagaimana kontribusi dapat dilakukan. 😊