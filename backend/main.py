# Standard:
import os
import json
from typing import Dict, List, Any

# PyPI:
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()

# Local:
from common.config import chatgpt_35_turbo
from common.prompts import system_prompt 
from common.generate import generate_response

model = chatgpt_35_turbo['name']

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(question: Question):
    answer = generate_response(system_prompt=system_prompt, user_prompt=question.question, model=model)
    return {"question": question.question, "answer": answer}


