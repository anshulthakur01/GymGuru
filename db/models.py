from db.database import engine, Base
from sqlalchemy import Column, Integer, String, Enum, Date, Text, JSON, ForeignKey
from utils.enums import Gender, FitnessGoal, MemberShip
from db.common_models import TimestampMixin
from sqlalchemy.orm import declarative_base



class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    gender = Column(String, Enum(Gender))
    date_of_birth = Column(Date)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    address = Column(Text)
    fitness_goal = Column(String, Enum(FitnessGoal))
    membership = Column(String, Enum(MemberShip))


class Chat(Base, TimestampMixin):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class ChatHistory(Base, TimestampMixin):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    response = Column(Text)
    file_dict = Column(JSON, default={"name": None, "base64": None})
    chat_id = Column(Integer, ForeignKey("chats.id"))
    message_order = Column(Integer, default=0)  # To maintain message order


Base.metadata.create_all(bind=engine)