#!/bin/bash

# Buat virtual environment
python3 -m venv venv

# Aktifkan dan install dependensi dasar
source venv/bin/activate
pip install --upgrade pip
pip install flask python-dotenv

# Buat requirements.txt dari dependensi yang sudah terinstal
pip freeze > requirements.txt

# Buat file .gitignore kalau belum ada
cat > .gitignore <<EOF
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtualenv
venv/
ENV/
env/
.venv/

# Flask
instance/
A*.db

# dotenv
.env
.env.*

# Logs
*.log
logs/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF

# Buat file .env contoh
cat > .env <<EOF
API_ENDPOINT=http://localhost:5050/api/data
EOF

echo "✅ Setup selesai! Aktifkan venv dengan: source venv/bin/activate"
