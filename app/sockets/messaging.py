from flask_socketio import emit, join_room, leave_room
from flask import request
from app.extensions import db
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant

active_chambers = {}
sid_to_user = {}

def register_messaging_events(socketio):
    @socketio.on("message:join")
    def join_chat(data):
        print("🔥 JOIN REQUEST RECEIVED:", data)
        print("🚨 JOIN HANDLER CALLED SID:", request.sid)
        print("🚨 DATA:", data)
        conversation_id, user_id = data.get("conversation_id"), data.get("user_id")
        if not conversation_id: return
        participant = ( ConversationParticipant.query
            .filter_by(  conversation_id=conversation_id,  user_id=user_id, )
            .first() )
        if not participant:
            print( f"❌ Unauthorized join attempt: " f"user={user_id}, conversation={conversation_id}")
            return
        
        if user_id:
            active_chambers[int(user_id)] = int(conversation_id)
            sid_to_user[request.sid] = int(user_id)
            print("👁 ACTIVE CHAMBERS:", active_chambers)
        room = f"conversation_{conversation_id}"
        join_room(room)
        print("🔥 USER JOINED ROOM:", room)
        emit("room:joined", {"room": room})
        if user_id:
           active_chambers[int(user_id)] = int(conversation_id)
           sid_to_user[request.sid] = int(user_id)


    @socketio.on("message:leave")
    def leave_chat(data):
        print("🚪 LEAVE REQUEST RECEIVED:", data)
        user_id, conversation_id = data.get("user_id"), data.get("conversation_id")
        if user_id: active_chambers.pop(int(user_id), None) 
        if conversation_id: leave_room(f"conversation_{conversation_id}") 
        print("🧹 ACTIVE CHAMBERS AFTER LEAVE:", active_chambers)

    @socketio.on("chamber:open")
    def chamber_open(data):
        user_id = data.get("user_id")
        conversation_id = data.get("conversation_id")

        if not user_id or not conversation_id:
          return

        active_chambers[int(user_id)] = int(conversation_id)

    print("ACTIVE CHAMBER:", active_chambers)


    @socketio.on("chamber:close")
    def chamber_close(data):
         user_id = data.get("user_id")

         if not user_id:
              return

         active_chambers.pop(int(user_id), None)

    print("INACTIVE CHAMBER:", active_chambers)

