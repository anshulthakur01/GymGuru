from db.models import Chat, ChatHistory
from sqlalchemy.orm import Session


def get_chat_with_id(id: int, db: Session) -> Chat: 
    """
    Get a chat with id
    """
    return db.query(Chat).filter(Chat.id == id).first()


def get_chat_history_with_chat_id(chat_id: int, db: Session) -> ChatHistory:
    """
    Get a chat history with chat id
    """
    return db.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).order_by(ChatHistory.created_at.desc()).all()


def create_chat(data: dict, db: Session) -> None:
    """
    Create a chat in the database
    """

    chat = Chat(
        title=data["title"],
    )
    db.add(chat)
    db.commit()
    return chat