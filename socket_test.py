import socketio
import time

# =========================
# JWT TOKEN
# =========================
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3ODM0NjI2OSwianRpIjoiOTdhMDQ1NGItOGRiZS00MjViLTljNjAtMTkwYzgxZTkyOWViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjUiLCJuYmYiOjE3NzgzNDYyNjksImNzcmYiOiIwNDcwNzcyZC03NWY1LTQyZmYtYTE0ZC1kOWE3NTAzNzZjY2YiLCJleHAiOjE3NzgzNDcxNjl9.p1exIUT4gRiUoPBME4jApwq6tNhG_aaQIhuUSlWQOso"

sio = socketio.Client()


# =========================
# CONNECT
# =========================
@sio.event
def connect():
    print("✅ Connected to server")

    # Join a conversation (optional)
    sio.emit("join_conversation", {
        "conversation_id": 1
    })

    print("📥 Joined conversation 1")

    # simulate activity delay so we can test online status
    print("⏳ Staying online for 5 seconds to simulate active user...")
    time.sleep(5)


# =========================
# DISCONNECT
# =========================
@sio.event
def disconnect():
    print("❌ Disconnected from server")
    print("🕒 This should trigger last_seen update on backend")


# =========================
# SOCKET EVENTS (optional debug)
# =========================
@sio.on("user_typing")
def typing(data):
    print("✏️ typing:", data)


@sio.on("user_stop_typing")
def stop_typing(data):
    print("🛑 stop typing:", data)


# =========================
# RUN TEST
# =========================
print("Connecting...")

sio.connect(f"http://127.0.0.1:5000?token={TOKEN}")

# keep connection alive for a bit
time.sleep(5)

print("🔌 Closing connection to trigger last_seen...")
sio.disconnect()

print("Done.")