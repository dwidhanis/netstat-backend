# 📡 Netstat Backend

Sebuah proyek monitoring pemakaian WiFi berbasis Flask dan vnStat, dilengkapi dashboard visual dengan Chart.js.

---

## ⚙️ Fitur Utama

- REST API backend menggunakan Flask
- Otomatis ambil data penggunaan dari `vnstat`
- Mengirim data ke backend secara periodik atau real-time
- Dashboard frontend berbasis HTML + Chart.js
- Integrasi systemd untuk startup otomatis
- Dukungan `.env` untuk konfigurasi fleksibel

---


---

## 🚀 Cara Menjalankan

```bash
# Aktifkan environment
source venv/bin/activate

# Jalankan backend Flask
python app.py

# Atau jalankan stack penuh
bash start_all.sh

📦 Setup Environment (sekali saja)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
