#!/usr/bin/env bash
# Setup moi truong cho du an house_price_ml (Linux/macOS)
# Chay: bash setup_env.sh   (dung tu trong thu muc goc du an)
set -e

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Xong. Lan sau chi can chay: source .venv/bin/activate"
python -c "import sklearn, xgboost; print('OK', sklearn.__version__, xgboost.__version__)"
