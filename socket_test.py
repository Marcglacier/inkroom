import socketio

# =========================
# INSERT A VALID JWT TOKEN
# =========================
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3ODMzNzYyOSwianRpIjoiNGNiOGQ1YTAtM2Y4MC00ZDRhLWIzZTEtNjIzMjVjZGEzZTMyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjUiLCJuYmYiOjE3NzgzMzc2MjksImNzcmYiOiJhMTczZTNhYS1hMDQ3LTRlZTUtYjI1ZC00MzNhNTY0MDk2NmMiLCJleHAiOjE3NzgzMzg1Mjl9.Bm2ry0xCkoT3RrQgeEwx-3PipmG-EGn8qHPzJT0SRKY"

sio = socketio.Client()


# =========================
# CONNECTION EVENTS
# =========================
@sio.event
def connect():
    print("✅ Connected to server")

    # Join conversation room
    sio.emit("join_conversation", {
        "conversation_id": 1
    })

    print("Joined conversation 1")

    # Simulate typing
    sio.emit("typing_start", {
        "conversation_id": 1
    })


@sio.event
def disconnect():
    print("❌ Disconnected from server")


# =========================
# SERVER EVENTS
# =========================
@sio.on("user_typing")
def user_typing(data):
    print("✏️ User typing:", data)


@sio.on("user_stop_typing")
def user_stop_typing(data):
    print("🛑 User stopped typing:", data)


print("Connecting...")

# =========================
# CONNECT WITH JWT TOKEN
# =========================
sio.connect(
    f"http://127.0.0.1:5000?token={TOKEN}"
)

input("Press ENTER to simulate stop typing...\n")

sio.emit("typing_stop", {
    "conversation_id": 1
})

input("Press ENTER to exit...\n")