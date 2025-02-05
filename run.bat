@echo off
IF NOT EXIST "venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activate the virtual environment...
.\venv\Scripts\activate

@REM IF %ERRORLEVEL% NEQ 0 (
@REM     echo Installing requirements.txt...
@REM     python -m pip install -r requirements.txt
@REM ) ELSE (
@REM     echo Updating requirements.txt...
@REM     python -m pip install --upgrade pip
@REM     python -m pip install -r requirements.txt
@REM )

REM Run the server
@REM streamlit run app.py