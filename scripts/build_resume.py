"""Gera curriculo-andre-graccia.pdf (curriculo.html) e resume-andre-graccia-en.pdf (resume-en.html) (PDF com texto real, A4, sem cabeçalho do navegador).
Uso: python scripts/build_resume.py   (precisa do Google Chrome instalado)"""
import os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = next((p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                           "/usr/bin/google-chrome", "/usr/bin/chromium") if os.path.exists(p)), None)
if not CHROME:
    sys.exit("Chrome não encontrado")
for src, dst in (("curriculo.html", "curriculo-andre-graccia.pdf"), ("resume-en.html", "resume-andre-graccia-en.pdf")):
    out = os.path.join(ROOT, dst)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                    "file:///" + os.path.join(ROOT, src).replace("\\", "/")], check=True, capture_output=True)
    print("ok", out, os.path.getsize(out), "bytes")
