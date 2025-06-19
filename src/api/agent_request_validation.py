# src/api/validation.py

from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
import os

load_dotenv()
MAX_INPUT_LENGTH = os.getenv("MAX_INPUT_LENGTH", 5000)
    
def validate_input(text: str, max_length: int = int(MAX_INPUT_LENGTH) | 5000) -> None:
    if not text.strip():
        raise ValueError("Message cannot be empty.")
    if len(text) > max_length:
        raise ValueError(f"Message exceeds max length of {max_length} characters.")
