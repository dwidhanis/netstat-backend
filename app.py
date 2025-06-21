from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import json

app = Flask(__name__)

# Konfigurasi database SQLite (akan dibuat di folder yang sama)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wifi_monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Model Database ---
class WifiData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    interface = db.Column(db.String(50), nullable=False)
    total_rx = db.Column(db.BigInteger, nullable=False) # Total bytes received (download)
    total_tx = db.Column(db.BigInteger, nullable=False) # Total bytes transmitted (upload)
    # Anda bisa menyimpan data mentah vnstat juga jika diperlukan untuk analisis lebih lanjut
    raw_data_json = db.Column(db.Text)

    def __repr__(self):
        return f"<WifiData {self.timestamp} - {self.interface}>"

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'interface': self.interface,
            'total_rx': self.total_rx,
            'total_tx': self.total_tx,
            'raw_data_json': self.raw_data_json
        }

# --- API Endpoints ---
@app.route('/api/data', methods=['POST'])
def receive_wifi_data():
    data = request.json
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400

    try:
        new_data = WifiData(
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            interface=data['interface'],
            total_rx=data['total_rx'],
            total_tx=data['total_tx'],
            raw_data_json=json.dumps(data.get('raw_vnstat_data')) # Simpan data mentah sebagai string JSON
        )
        db.session.add(new_data)
        db.session.commit()
        print(f"Data received and saved: {new_data}")
        return jsonify({"message": "Data received and saved", "id": new_data.id}), 201
    except KeyError as e:
        return jsonify({"message": f"Missing data: {e}"}), 400
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"message": f"Internal server error: {e}"}), 500

@app.route('/api/data', methods=['GET'])
def get_wifi_data():
    # Ambil 100 data terbaru
    data_records = WifiData.query.order_by(WifiData.timestamp.desc()).limit(100).all()
    return jsonify([record.to_dict() for record in data_records])

@app.route('/')
def index():
    # Ini bisa digunakan untuk melayani file frontend HTML/CSS/JS nanti
    # Untuk sementara, hanya teks sederhana
    return "WiFi Monitor Backend is running. Access /api/data for data."

# --- Jalankan Aplikasi ---
if __name__ == '__main__':
    # Pastikan file database dibuat jika belum ada
    with app.app_context():
        db.create_all()
    # Jalankan di semua antarmuka (0.0.0.0) agar bisa diakses dari perangkat lain di jaringan
    # Debug=True hanya untuk pengembangan, matikan untuk produksi
    app.run(host='0.0.0.0', port=5050, debug=True)
