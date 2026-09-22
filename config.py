"""Shared configuration for the Student Academic Assistant."""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

else:
    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. Use groq."
    )


if not API_KEY:
    raise SystemExit(
        "No API key found. Check your .env file."
    )


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


with open("data/student_data.json", "r") as file:
    STUDENT_DATA = json.load(file)



QUESTIONS = [
    "What is my attendance percentage?",
    "What is my CGPA?",
    "Am I eligible for placement training?",
    "Do I have any pending fees?",
    "Check my academic information and tell me whether I am eligible for placement training and whether I have any pending fees."
]


def banner(system_name):
    print(
        f"\n=== {system_name} | "
        f"provider: {PROVIDER} | "
        f"model: {MODEL} ===\n"
    )