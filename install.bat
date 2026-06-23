@echo off
echo ========================================
echo JARVIS AI Assistant - Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"
if errorlevel 1 (
    echo ERROR: Python 3.7+ is required
    echo Please upgrade your Python installation
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo ========================================

pip install --upgrade pip

echo Installing core dependencies...
pip install eel
pip install pyttsx3
pip install speechrecognition
pip install pyaudio
pip install psutil
pip install requests
pip install pillow
pip install opencv-contrib-python
pip install numpy
pip install pyautogui
pip install pywhatkit
pip install schedule
pip install cryptography
pip install qrcode

echo.
echo Installing AI dependencies...
pip install groq
pip install google-generativeai
pip install hugchat

echo.
echo Installing optional dependencies...
pip install pvporcupine
pip install pygame
pip install gtts

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.

echo Setting up configuration...
if not exist "groq_config.py" (
    echo Creating groq_config.py...
    echo GROQ_API_KEY = "your-groq-api-key-here" > groq_config.py
)

if not exist "gemini_config.py" (
    echo Creating gemini_config.py...
    echo GEMINI_API_KEY = "your-gemini-api-key-here" > gemini_config.py
)

echo.
echo ========================================
echo SETUP INSTRUCTIONS:
echo ========================================
echo 1. Edit groq_config.py and add your Groq API key
echo 2. Edit gemini_config.py and add your Gemini API key
echo 3. For phone integration, enable USB debugging on Android
echo 4. Run: python run.py
echo.
echo For face authentication setup, run: python setup_face_auth.py
echo.
echo ========================================
echo Installation complete! Ready to run JARVIS.
echo ========================================

pause