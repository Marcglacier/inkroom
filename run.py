# run.py
from dotenv import load_dotenv

load_dotenv()

import os
import socket
import subprocess
from pathlib import Path

from app import create_app
from app.extensions import socketio
from app.infrastructure import start_monitoring


CERT_DIR = Path("certs/dev")
CERT_FILE = CERT_DIR / "server.pem"
KEY_FILE = CERT_DIR / "server-key.pem"


def get_local_ip() -> str:
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]
    finally:
        connection.close()


def ensure_certificate(local_ip: str) -> tuple[str, str]:
    CERT_DIR.mkdir(parents=True, exist_ok=True)

    if CERT_FILE.exists() and KEY_FILE.exists():
        print(f"🔐 USING EXISTING CERTIFICATE: {local_ip}")
        return str(CERT_FILE), str(KEY_FILE)

    print(f"🔐 GENERATING CERTIFICATE: {local_ip}")

    result = subprocess.run(
        [
            "mkcert",
            "-cert-file",
            str(CERT_FILE),
            "-key-file",
            str(KEY_FILE),
            local_ip,
            "localhost",
            "127.0.0.1",
        ],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Failed to generate HTTPS certificate."
        )

    if not CERT_FILE.exists():
        raise RuntimeError(
            f"Certificate was not created: {CERT_FILE}"
        )

    if not KEY_FILE.exists():
        raise RuntimeError(
            f"Certificate key was not created: {KEY_FILE}"
        )

    return str(CERT_FILE), str(KEY_FILE)


app = create_app()


if __name__ == "__main__":

    if (
        os.environ.get(
            "WERKZEUG_RUN_MAIN"
        ) == "true"
    ):
        start_monitoring(app)

    local_ip = get_local_ip()

    print(f" LOCAL NETWORK IP: {local_ip}")

    certificate, key = ensure_certificate(local_ip)

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        ssl_context=(certificate, key),
        allow_unsafe_werkzeug=True,
    )