#!/bin/bash
# startup script for Azure App Service (Linux)
# - run FastAPI backend in background
# - run Streamlit frontend as main process (exposed to outside)

set -e

echo "Starting startup.sh..."

cd /home/site/wwwroot || exit 1

# ✅ 한글 폰트 설치
echo "Installing Korean fonts..."
apt-get update && apt-get install -y fonts-nanum

# ✅ 로케일 설정
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8


# Activate Oryx-created virtualenv if present
if [ -d "/home/site/wwwroot/antenv" ]; then
  echo "Activating virtual environment: antenv"
  source /home/site/wwwroot/antenv/bin/activate
else
  echo "Virtual environment not found. Proceeding with system Python."
fi

# Install dependencies (optional, usually done at build time)
if [ -f "requirements.txt" ]; then
  echo "Installing requirements..."

  # Check if pip is available
  if ! command -v pip &> /dev/null; then
    echo "pip not found, trying python -m pip"
    python -m pip install -r requirements.txt
  else
    pip install -r requirements.txt
  fi
else
  echo "No requirements.txt found. Skipping dependency installation."
fi

# Start FastAPI backend on internal port (not exposed)
# echo "Starting FastAPI backend on port 8001..."
# uvicorn backend.main:app --host 0.0.0.0 --port 8001 --log-level info &

# Start Streamlit frontend on the external port ($PORT)
echo "Starting Streamlit frontend on port $PORT..."
exec streamlit run frontend/app2.py --server.port $PORT --server.address 0.0.0.0



