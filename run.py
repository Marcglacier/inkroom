# run.py
from dotenv import load_dotenv

load_dotenv()

import os
import socket

from app import create_app
from app.extensions import socketio
from app.infrastructure import start_monitoring


def get_local_ip() -> str:
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]
    finally:
        connection.close()

def ensure_certificate(local_ip: str) -> tuple[str, str]:
    certificate = f"{local_ip}+2.pem"
    key = f"{local_ip}+2-key.pem"

    if os.path.exists(certificate) and os.path.exists(key):
        print(f"🔐 USING EXISTING CERTIFICATE: {local_ip}")
        return certificate, key

    print(f"🔐 GENERATING CERTIFICATE: {local_ip}")

    result = os.system(
        f'mkcert {local_ip} localhost 127.0.0.1'
    )

    if result != 0:
        raise RuntimeError(
            "Failed to generate HTTPS certificate."
        )

    if not os.path.exists(certificate):
        raise RuntimeError(
            f"Certificate was not created: {certificate}"
        )

    if not os.path.exists(key):
        raise RuntimeError(
            f"Certificate key was not created: {key}"
        )

    return certificate, key

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