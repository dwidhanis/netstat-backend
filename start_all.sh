#!/bin/bash
cd /root/netstat-backend
source venv/bin/activate

# Jalankan Flask di background pakai tmux
tmux new-session -d -s netstat-flask "python app.py"

# Jalankan kolektor looping (pastikan sudah looping di dalam script)
python collect_data.py
