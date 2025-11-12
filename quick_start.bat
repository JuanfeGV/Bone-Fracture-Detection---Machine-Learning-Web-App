@echo off
REM Script de inicio rápido para la aplicación de Detección de Fracturas
REM Ejecutar: quick_start.bat

echo.
echo ====================================================================
echo DETECCIÓN DE FRACTURAS - INICIO RÁPIDO
echo ====================================================================
echo.

REM Verificar que pip está disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no está disponible
    echo Por favor instala Python 3.12+ desde python.org
    pause
    exit /b 1
)

echo Paso 1: Instalando dependencias...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if errorlevel 1 (
    echo ERROR: Falló la instalación de dependencias
    pause
    exit /b 1
)

echo OK
echo.
echo Paso 2: Iniciando la aplicación...
echo.
echo La aplicación se abrirá en: http://127.0.0.1:5000
echo.
echo Credenciales:
echo   Usuario: admin
echo   Contraseña: fractura123
echo.
echo Presiona Ctrl+C en esta ventana para detener la aplicación
echo.
echo ====================================================================
echo.

python app.py

pause
