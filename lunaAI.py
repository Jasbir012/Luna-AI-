from google import genai
import os, json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file!")

client = genai.Client(api_key=api_key)
HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history_entry(user_input, ai_response):
    history = load_history()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_input,
        "assistant": ai_response
    }
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def get_ai_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        ai_text = response.text.strip()
        save_history_entry(prompt, ai_text)
        return ai_text
    except Exception as e:
        return f"Error: {e}"
