from fastapi import FastAPI, WebSocket, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from utils.chat_service import ChatService
from db.database import get_db
from db.models import Chat, ChatHistory

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/chats")
def get_chats(db: Session = Depends(get_db)):
    """Get all chats"""
    chats = db.query(Chat).order_by(Chat.created_at.desc()).all()
    return [{"id": chat.id, "title": chat.title, "created_at": chat.created_at} for chat in chats]


@app.get("/api/chats/{chat_id}/history")
def get_chat_history(chat_id: int, db: Session = Depends(get_db)):
    """Get chat history for a specific chat"""
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    history = db.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).order_by(ChatHistory.message_order).all()
    return {
        "chat": {"id": chat.id, "title": chat.title},
        "history": [{"message": h.message, "response": h.response, "created_at": h.created_at} for h in history]
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Initialize chat service without creating a chat yet
    chat_service = ChatService(operation="registeration")

    while True:
        data = await websocket.receive_text()
        print("Data received from websockets :", data)
        response = chat_service.process_response(data)
        await websocket.send_text(response)