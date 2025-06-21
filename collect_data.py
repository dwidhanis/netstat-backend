import json
import subprocess
import requests
import datetime
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()  # otomatis baca file .env

# URL endpoint API backend Anda
# Jika backend juga berjalan di HG680P, gunakan alamat IP lokal HG680P
# Contoh: http://192.168.1.100:5000/api/data
# Ganti dengan IP HG680P Anda dan port yang akan Anda gunakan untuk backend Flask
API_ENDPOINT = os.getenv("API_ENDPOINT") # Untuk pengujian awal, jika backend juga di HG680P
INTERFACE_NAME = "eth0" # Sesuaikan dengan antarmuka jaringan Anda

def get_vnstat_data():
    """Mengambil data penggunaan dari vnstat dalam format JSON."""
    try:
        # Jalankan perintah vnstat untuk mendapatkan data JSON
        # Output JSON dari vnstat seringkali cukup detail, kita ambil ringkasan bulan ini atau hari ini
        result = subprocess.run(['vnstat', '--json', 'm'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data
    except subprocess.CalledProcessError as e:
        print(f"Error calling vnstat: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from vnstat: {e}")
        return None

def send_data_to_api(data):
    """Mengirim data ke API backend."""
    try:
        response = requests.post(API_ENDPOINT, json=data, timeout=10)
        response.raise_for_status() # Akan memunculkan error untuk status kode 4xx/5xx
        print(f"Data sent successfully. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Starting data collection...")
    vnstat_raw_data = get_vnstat_data()

    if vnstat_raw_data and vnstat_raw_data['interfaces']:
        # Ambil data untuk antarmuka yang spesifik
        interface_data = next((iface for iface in vnstat_raw_data['interfaces'] if iface['name'] == INTERFACE_NAME), None)

        if interface_data:
            # Contoh sederhana: ambil data bulan ini
            current_month_data = None
            if interface_data['traffic']['month']:
                current_month_data = interface_data['traffic']['month'][-1] # Ambil bulan terakhir

            payload = {
                "timestamp": datetime.datetime.now().isoformat(),
                "interface": INTERFACE_NAME,
                "total_rx": current_month_data['rx'] if current_month_data else 0, # Total received (download)
                "total_tx": current_month_data['tx'] if current_month_data else 0, # Total transmitted (upload)
                # Anda bisa menambahkan data lain dari vnstat_raw_data jika diperlukan
                "raw_vnstat_data": vnstat_raw_data # Kirim data mentah juga
            }
            send_data_to_api(payload)
        else:
            print(f"Interface '{INTERFACE_NAME}' not found in vnstat data.")
    else:
        print("No vnstat data or interfaces found.")

    print(f"[{datetime.datetime.now()}] Data collection finished.")
