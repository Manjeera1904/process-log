import os
from google import genai

def analyze_file(file_path):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "### ❌ Error\nGOOGLE_API_KEY not found."

    client = genai.Client(api_key=api_key)
    
    if not os.path.exists(file_path):
        return f"### ❌ Error\nFile `{file_path}` not found."

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # We tell the AI EXACTLY how to format the response
    system_prompt = (
        "You are a Senior QA Automation Lead. Analyze the provided test code. "
        "Your output MUST be a Markdown table with the following columns: "
        "Issue Type, Line Number, Description, and Recommended Fix. "
        "Focus on: Hardcoded locators, Weak waits (Thread.sleep), and Missing assertions."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Analyze this code:\n\n{code}",
            config={"system_instruction": system_prompt}
        )
        return response.text
    except Exception as e:
        return f"### ❌ AI Analysis Failed\n{str(e)}"