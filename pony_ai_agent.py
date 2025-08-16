import os
import json
import requests
from pathlib import Path

# === CONFIG ===
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder"  # or "codellama", etc.
PROJECT_PATH = Path(r"C:\Users\joshu\Desktop\ponyxpress")
FILE_EXTENSIONS = [".py", ".html", ".js", ".css", ".txt", ".md"]
BASE_PATH = r"C:\Users\joshu\Desktop\ponyxpress"

# === PROMPT ===
SYSTEM_PROMPT = """You are a professional software engineer tasked with improving and completing the PonyXpress app. 
You have full access to the source files. Fix any issues, fill in missing logic, remove placeholders, and optimize all code. 
Never include sample code or incomplete logic. Make all necessary changes for this app to be fully functional.
"""

# === FUNCTION ===
def send_to_ollama(prompt, content):
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser Instruction:\n{prompt}\n\nCode:\n{content}"
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print("Error:", e)
        return None

def process_file(file_path, prompt="Improve this file completely and remove all placeholders."):
    print(f"🔧 Processing: {file_path.name}")
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        original = f.read()

    ai_response = send_to_ollama(prompt, original)
    if ai_response:
        # Backup
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        file_path.rename(backup_path)
        print(f"📦 Backup saved: {backup_path.name}")

        # Write updated file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(ai_response)
        print(f"✅ Updated: {file_path.name}")
    else:
        print(f"⚠️ Failed to process: {file_path.name}")

def write_file(relative_path, content):
    full_path = os.path.join(BASE_PATH, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Wrote: {full_path}")

def main():
    print(f"🚀 Scanning folder: {PROJECT_PATH}")
    for ext in FILE_EXTENSIONS:
        for file in PROJECT_PATH.rglob(f"*{ext}"):
            process_file(file)

if __name__ == "__main__":
    main()
