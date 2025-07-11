# Register user tool for gemini api
REGISTER_USER_TOOL_DECLARATION = {
    "name": "register_user",
    "description": "Register a user in the database.",
    "parameters": {
        "type": "object",
        "properties": {
            "full_name": {
                "type": "string",
                "description": "Full name of the user.",
            },
            "gender": {
                "type": "string",
                "description": "Gender of the user.",
            },
            "date_of_birth": {
                "type": "string",
                "description": "Date of birth of the user.",
            },
            "email": {
                "type": "string",
                "description": "Email of the user.",
            },
            "phone_number": {
                "type": "string",
                "description": "Phone number of the user.",
            },
            "address": {
                "type": "string",
                "description": "Address of the user.",
            },
            "fitness_goal": {
                "type": "string",
                "description": "Fitness goal of the user.",
            },
            "membership": {
                "type": "string",
                "description": "Membership of the user.",
            },
        },
        "required": ["full_name", "gender", "date_of_birth", "email", "phone_number", "address", "fitness_goal", "membership"],
    },
}