import json
from tqdm import tqdm

# Membaca data dari file JSON
print("Membaca data dari file JSON...")
with open('datasets/laravel_dataset.json', 'r') as file:
    data = json.load(file)

# Menggunakan dictionary untuk menyimpan item unik
print("Memproses data untuk menghapus duplikat...")
unique_items = {}
for item in tqdm(data, desc="Memproses item", unit="item"):
    # Menggunakan tuple dari item sebagai kunci untuk menghindari duplikat
    key = (item['question'], item['answer'], item['code'], item['source'])
    unique_items[key] = item

# Mengonversi kembali ke list
unique_data = list(unique_items.values())

# Menghitung jumlah item yang tersisa
count = len(unique_data)

# Menyimpan hasil ke file JSON baru
output_file = 'datasets/laravel_dataset_unique.json'
print(f"Menyimpan hasil ke file: {output_file}")
with open(output_file, 'w') as file:
    json.dump(unique_data, file, indent=4)

# Menampilkan ringkasan
print(f"Jumlah item awal: {len(data)}")
print(f"Jumlah item unik: {count}")
print(f"File JSON baru telah disimpan: {output_file}")