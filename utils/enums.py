from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class FitnessGoal(Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_BUILDING = "muscle_building"
    GENERAL_FITNESS = "general_fitness"
    SPORTS_TRAINING = "sports_training"


class MemberShip(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


FITNESS_GOAL_DESCRIPTIONS = {
    FitnessGoal.WEIGHT_LOSS.value: "Focuses on reducing body fat through cardio and calorie deficit.",
    FitnessGoal.MUSCLE_BUILDING.value: "Targets muscle gain through strength training and nutrition.",
    FitnessGoal.GENERAL_FITNESS.value: "Improves overall health, stamina, and energy levels.",
    FitnessGoal.SPORTS_TRAINING.value: "Enhances performance for specific sports with agility and power workouts."
}


MEMBERSHIP_DETAILS = {
    MemberShip.BASIC.value: {
        "duration": "1 Month",
        "price": 2000,
        "price_per_month": 2000,
        "description": "Basic access to gym equipment. Ideal for trying out or short-term users."
    },
    MemberShip.STANDARD.value: {
        "duration": "3 Months",
        "price": 4000,
        "price_per_month": 1333,
        "description": "Includes gym access and limited group classes. Great for regular users."
    },
    MemberShip.PREMIUM.value: {
        "duration": "6 Months",
        "price": 6000,
        "price_per_month": 1000,
        "description": "Full access to all facilities, including group classes and trainer sessions."
    }
}