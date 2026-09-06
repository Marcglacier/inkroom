# run.py
from dotenv import load_dotenv

load_dotenv()

import os

from app import create_app
from app.extensions import socketio
from app.infrastructure import start_monitoring


app = create_app()


if __name__ == "__main__":

    if (
        os.environ.get(
            "WERKZEUG_RUN_MAIN"
        ) == "true"
    ):

        start_monitoring(app)

    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
    )