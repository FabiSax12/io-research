"""Reconstruye la presentación completa desde cero.

    python presentacion/reconstruir.py              # modelos (run_all.py) + gráficos + PPTX
    python presentacion/reconstruir.py --sin-modelos  # solo gráficos + PPTX con los resultados que ya existen
    python presentacion/reconstruir.py --pdf          # además exporta PDF y miniaturas PNG (requiere LibreOffice)

Salida: presentacion/salida/presentacion_io.pptx (y .pdf / previews/ con --pdf).
Se puede correr desde cualquier carpeta.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SALIDA = AQUI / "salida"


def paso(texto):
    print(f"\n==> {texto}", flush=True)


def correr_modelos():
    paso("Resolviendo los modelos (run_all.py: Python y, si está instalado, R)")
    r = subprocess.run([sys.executable, str(RAIZ / "run_all.py")], cwd=RAIZ)
    if r.returncode != 0:
        print("Aviso: run_all.py terminó con diferencias o fallos (por ejemplo, R no instalado). "
              "La presentación se arma igual y marca lo que falta como pendiente.")


def revisar_fuentes():
    """Las fuentes deben estar instaladas en la máquina que abre el PPTX; aquí solo se avisa."""
    try:
        from matplotlib import font_manager
        nombres = {f.name for f in font_manager.fontManager.ttflist}
    except Exception:
        return
    if "Onest" not in nombres or "Barlow Condensed" not in nombres:
        print(f"Aviso: instale las fuentes de {AQUI / 'fuentes'} (Onest y Barlow Condensed) en el sistema "
              "para que PowerPoint muestre el diseño correcto. Los gráficos ya las usan desde esa carpeta.")


def exportar_pdf(pptx):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print("Aviso: no se encontró LibreOffice (soffice); se omite el PDF.")
        return
    paso("Exportando PDF con LibreOffice")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(SALIDA), str(pptx)],
                   check=False, capture_output=True)
    pdf = SALIDA / (pptx.stem + ".pdf")
    if not pdf.exists():
        print("Aviso: LibreOffice no generó el PDF.")
        return
    print(f"PDF: {pdf}")
    if shutil.which("pdftoppm"):
        previews = SALIDA / "previews"
        shutil.rmtree(previews, ignore_errors=True)
        previews.mkdir()
        subprocess.run(["pdftoppm", "-r", "96", "-png", str(pdf), str(previews / "lamina")], check=False)
        print(f"Miniaturas: {previews}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-modelos", action="store_true", help="no correr run_all.py; usar resultados/ y capturas/ existentes")
    ap.add_argument("--pdf", action="store_true", help="exportar también PDF y miniaturas (LibreOffice)")
    ap.add_argument("--salida", help="ruta del .pptx (por defecto presentacion/salida/presentacion_io.pptx)")
    a = ap.parse_args()

    if not a.sin_modelos:
        correr_modelos()
    revisar_fuentes()
    paso("Generando gráficos y armando la presentación")
    sys.path.insert(0, str(AQUI))
    import construir
    pptx = construir.construir(a.salida)
    if a.pdf:
        exportar_pdf(Path(pptx))


if __name__ == "__main__":
    main()
