import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the application."""

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cab_management.db")

    # App Settings
    APP_NAME = "Intercity Cab Management"
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Authentication & Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Additional settings can be added here


# Initialize config instance
config = Config()
