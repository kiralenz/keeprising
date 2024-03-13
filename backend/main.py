# Standard:
import os
import json
from typing import Dict, List, Any

# PyPI:
from dotenv import load_dotenv

load_dotenv()

# Local:
from common.config import chatgpt_35_turbo
from common.prompts import system_prompt 
from common.generate import generate_response

model = chatgpt_35_turbo['name']

user_input = "I took the wrong flour to feed my sourdough. Is that a problem?"

print(generate_response(system_prompt=system_prompt, user_prompt=user_input, model=model))