"""Inicializador inteligente do Football Analytics Hub com verificação de prontidão e abertura de app."""

import sys
import os
import time
import subprocess
import urllib.request
import webbrowser
import socket

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def is_server_ready(url="http://localhost:8501/_stcore/health"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1) as resp:
            return resp.getcode() == 200
    except Exception:
        return False

def open_app_window(url="http://localhost:8501"):
    # 1. Tenta Microsoft Edge em App Mode (janela nativa sem barra)
    edge_paths = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for p in edge_paths:
        if os.path.exists(p):
            subprocess.Popen([p, f"--app={url}"])
            return "Microsoft Edge (Modo App Nativo)"

    # 2. Tenta Google Chrome em App Mode
    chrome_paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in chrome_paths:
        if os.path.exists(p):
            subprocess.Popen([p, f"--app={url}"])
            return "Google Chrome (Modo App Nativo)"

    # 3. Fallback: navegador padrão do sistema
    webbrowser.open(url)
    return "Navegador Padrão"

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    lan_ip = get_lan_ip()

    print("=" * 65)
    print("      ⚽ FOOTBALL ANALYTICS HUB — INICIANDO APLICATIVO")
    print("=" * 65)
    print("\n[1/3] Verificando se o servidor já está ativo...")

    server_process = None
    if not is_server_ready():
        print("[2/3] Iniciando servidor Streamlit local...")
        server_cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        server_process = subprocess.Popen(server_cmd)

        # Aguarda ativamente o servidor responder HTTP 200 (timeout 30 segundos)
        print("      Aguardando carregamento dos módulos de dados e IA...", end="", flush=True)
        started = False
        for _ in range(60):
            time.sleep(0.5)
            print(".", end="", flush=True)
            if is_server_ready():
                started = True
                break

        print("\n")
        if not started:
            print("❌ O servidor demorou mais que o esperado para iniciar.")
            print("Pressione qualquer tecla para tentar abrir manualmente...")
            input()
    else:
        print("✅ Servidor já estava rodando na porta 8501!\n")

    print("[3/3] Abrindo janela de aplicativo...")
    browser_used = open_app_window("http://localhost:8501")
    print(f"      Conectado com sucesso via {browser_used}!\n")

    print("=" * 65)
    print("   ✅ APLICATIVO PRONTO E DISPONÍVEL!")
    print("=" * 65)
    print(f"   💻 NO SEU COMPUTADOR: http://localhost:8501")
    print(f"   📱 NO SEU CELULAR (Android/iPhone no mesmo Wi-Fi):")
    print(f"      👉 http://{lan_ip}:8501")
    print("=" * 65)
    print("\n⚠️  ATENÇÃO:")
    print("   * Mantenha esta janela aberta enquanto estiver usando o app.")
    print("   * Para fechar o aplicativo, basta fechar esta janela.\n")

    try:
        if server_process:
            server_process.wait()
        else:
            # Mantém processo vivo para instrução do usuário
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        if server_process:
            server_process.terminate()
        print("\nAplicativo finalizado.")

if __name__ == "__main__":
    main()
