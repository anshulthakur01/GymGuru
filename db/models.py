from db.database import engine, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, Date, Text, JSON, ForeignKey
from utils.enums import Gender, FitnessGoal, MemberShip
from db.common_models import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    gender = Column(String, Enum(Gender))
    date_of_birth = Column(Date)
    email = Column(String, nullable=True)
    phone_number = Column(String, unique=True)
    address = Column(Text, nullable=True)
    fitness_goal = Column(String, Enum(FitnessGoal))
    membership = Column(String, Enum(MemberShip))


class Chat(Base, TimestampMixin):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    chat_history = relationship("ChatHistory", back_populates="chat", cascade="all, delete-orphan")



class ChatHistory(Base, TimestampMixin):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    response = Column(Text)
    file_dict = Column(JSON, default={"name": None, "base64": None})
    chat_id = Column(Integer, ForeignKey("chats.id"))
    message_order = Column(Integer, default=0)  # To maintain message order

    chat = relationship("Chat", back_populates="chat_history")


Base.metadata.create_all(bind=engine)