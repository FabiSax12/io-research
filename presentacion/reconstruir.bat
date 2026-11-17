@echo off
REM Reconstruye la presentacion (modelos + graficos + PPTX). Argumentos extra: --sin-modelos, --pdf
cd /d "%~dp0.."
python presentacion\reconstruir.py %*
