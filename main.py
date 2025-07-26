import os
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi", logger=True, engineio_logger=True, eio=4)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO on FastAPI
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Socket.IO Events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def ping(sid, data):
    print(f"Ping received at {int(__import__('time').time() * 1000)} from {sid}")
    await sio.emit("pong", {"time": int(__import__('time').time() * 1000)}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(sio_app, host="0.0.0.0", port=port)
