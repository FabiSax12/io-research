#!/usr/bin/env bash
# Reconstruye la presentación (modelos + gráficos + PPTX). Argumentos extra: --sin-modelos, --pdf
set -e
cd "$(dirname "$0")/.."
python presentacion/reconstruir.py "$@"
