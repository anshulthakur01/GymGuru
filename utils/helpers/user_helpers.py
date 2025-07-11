from db.models import User
from sqlalchemy.orm import Session


def get_user_with_email(email: str, db: Session) -> User:
    """
    Get a user with email
    """
    return db.query(User).filter(User.email == email).first()


def register_user(data: dict, db: Session) -> None:
    """
    Register a user in the database
    """

    user = User(
        full_name=data.get("full_name"),
        gender=data.get("gender"),
        date_of_birth=data.get("date_of_birth"),
        email=data.get("email"),
        phone_number=data.get("phone_number"),
        address=data.get("address"),
        fitness_goal=data.get("fitness_goal"),
    )
    db.add(user)
    db.commit()
    return user