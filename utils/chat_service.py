import json

from google import genai
from google.genai import types
from google.genai import types
from sqlalchemy.orm import Session

from db.models import ChatHistory
from config import settings
from utils.helpers import create_chat, register_user
from utils.enums import FITNESS_GOAL_DESCRIPTIONS, MEMBERSHIP_DETAILS
from utils.tools_conf import REGISTER_USER_TOOL_DECLARATION

MODEL = "gemini-2.5-flash"

REGISTERATION_SYSTEM_PROMPT = """
You are a Q&A chatbot for a Gym called GymGuru. 
You are responsible to collect the user information for full_name, gender (Add exact value to json but use readable format: male/female/other), date_of_birth, email, phone_number, address, fitness_goal (Add exact value to json but use readable format: weight_loss/muscle_building/general_fitness/sports_training), membership (Add exact value to json but use readable format: basic/premium)

Rules:
    - You can only ask one question at a time with proper explanation.
    - You can only answer questions which are related to GymGuru or related to the gym (Such as fitness advices (if user ask)).
    - You can only proceed to next question if user has answered the current question.
    - Take refrence from these for fields related to them : {%s}, {%s}
    - Always return response in following example json format so i can parse the json directly
    {
        all_required_answered: true/false (Only true is all requireds answered),
        answered_count: total number of questions answered (in data object),
        total_questions: total number of questions to be answered,
        data: {
            "full_name": "John Doe", (required)
            "gender": "male", (required)
            "date_of_birth": "1990-01-01", (required)
            "email": "john.doe@example.com", (optional, Try to get email if user decline tell benefits of this field)
            "phone_number": "1234567890", (optional, Try to get phone number if user decline tell benefits of this field)
            "address": "123 Main St, Anytown, USA", (optional, Try to get address if user decline tell benefits of this field)
            "fitness_goal": "weight_loss", (required, Try to get fitness goal if user decline tell benefits of this field)
            "membership": "basic" (required)
        },
        "ai_message": current_question/Register the user if all required questions are answered and reply with polite message for successful registeration.
""" % (FITNESS_GOAL_DESCRIPTIONS, MEMBERSHIP_DETAILS)


class ChatService:
    """
    Chat service for the application
    """

    def __init__(self, operation: str, db: Session = None) -> None:
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.operation = operation
        self.history = []
        self.db = db
        self.chat_id = None
        self.function_call_mapping = {
            "register_user": self.create_user
        }

    def _get_config(self) -> None:
        """
        Get the config for the chat
        """
        # Configure tools for the chat (Register user tool etc)
        tools = types.Tool(function_declarations=[REGISTER_USER_TOOL_DECLARATION])

        return types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            tools=[tools]
        )

    @property
    def system_prompt(self) -> str:
        """
        Get the system prompt for the chat
        """
        if self.operation == "registeration":
            return REGISTERATION_SYSTEM_PROMPT
        else:
            raise ValueError(f"Invalid operation: {self.operation}")

    def get_user_message(self, user_message: str) -> str:
        """
        Get the user message for the chat
        """
        self.history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))
        # keep only last 3 messages
        self.history = self.get_previous_history()
        return self.history
    
    def get_previous_history(self):
        """" 
        Get centralized chat history 
        """
        return self.history[-3:len(self.history)]

    def _create_chat_if_not_exists(self) -> None:
        """
        Create a new chat if it doesn't exist
        """
        if self.db and self.chat_id is None:
            chat_data = {"title": f"GymGuru Registration Chat - {self.operation}"}
            chat = create_chat(chat_data, self.db)
            self.chat_id = chat.id

    def _store_chat_history(self, user_message: str, ai_response: str) -> None:
        """
        Store chat history in the database
        """
        if self.db and self.chat_id:
            # Get the next message order
            last_message = self.db.query(ChatHistory).filter(ChatHistory.chat_id == self.chat_id).order_by(ChatHistory.message_order.desc()).first()
            next_order = (last_message.message_order + 1) if last_message else 0

            chat_history = ChatHistory(
                message=user_message,
                response=self.clean_response(ai_response),
                chat_id=self.chat_id,
                message_order=next_order
            )
            self.db.add(chat_history)
            self.db.commit()

    def generate_response(self, data: str) -> str:
        """
        Generate the response for the chat
        """
        data = json.loads(data)
        user_message = data.get("message")
        if not user_message:
            raise ValueError("User message is required")

        # Create chat if not exists
        self._create_chat_if_not_exists()

        user_message = self.get_user_message(user_message)

        response = self.client.models.generate_content(
            model=MODEL,
            contents=user_message,
            config=self._get_config()
        )

        # Check for function calling
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            reg_res = self.function_call_mapping.get(function_call.name)(function_call.args)
            user_dct = {
                "full_name": reg_res.full_name,
                "gender": reg_res.gender,
                "date_of_birth": reg_res.date_of_birth,
                "email": reg_res.email,
                "phone_number": reg_res.phone_number,
                "address": reg_res.address,
                "fitness_goal": reg_res.fitness_goal
            }

            # Generate a custom message to user when rgistered
            custom_message = f"""Response from server on register : {user_dct}, Previous History : {self.get_previous_history()}"""
            response = self.client.models.generate_content(
                model=MODEL,
                contents=custom_message,
                config=self._get_config()
            )

        self.history.append(types.Content(role="model", parts=[types.Part.from_text(text=response.text)]))

        # Store chat history - pass the original user message string and AI response text
        self._store_chat_history(data.get("message"), response.text)

        return self.clean_response(response.text)

    def clean_response(self, response: str) -> str:
        """
        Clean the response for the chat and return the json object
        """
        return response.replace("```json", "").replace("```", "").strip()

    def create_user(self, data: dict) -> None:
        """
        Register the user in the database
        """
        return register_user(data, self.db)