@echo off
REM Setup moi truong cho du an house_price_ml (Windows)
REM Chay: setup_env.bat  (dung tu trong thu muc goc du an)

python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Xong. Lan sau chi can chay: .venv\Scripts\activate.bat
echo Kiem tra: python -c "import sklearn, xgboost; print('OK', sklearn.__version__, xgboost.__version__)"
