import os
from google import genai

def analyze_file(file_path):
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not found."

    client = genai.Client(api_key=api_key)
    
    if not os.path.exists(file_path):
        return f"File {file_path} not found."

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    prompt = f"""
    Review this test code for:
    - Hardcoded locators (XPaths/CSS)
    - Weak waits (Thread.sleep)
    - Missing assertions
    
    Code to analyze:
    {code}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Analysis failed: {str(e)}"