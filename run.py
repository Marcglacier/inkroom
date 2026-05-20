# run.py
from app import create_app
from app.extensions import socketio
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)