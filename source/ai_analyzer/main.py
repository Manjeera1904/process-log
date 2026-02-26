import os
from google import genai
# Import your existing logic
from dead_code_detector import detect_dead_code
from static_analyzer import analyze_file  # Note: Ensure this matches your static_analyzer function name

def generate_ai_maintenance_report():
    # 1. Securely get the API Key from Environment Variables
    # The YAML will pass 'GOOGLE_API_KEY' here
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment!")
        return

    client = genai.Client(api_key=api_key)

    # 2. Get data from your existing scripts
    # Note: Ensure these functions return strings or lists
    dead_code_results = detect_dead_code()
    
    # Using the analyze_file function from your other script
    # You might need to loop through files or pass a specific one
    static_smells = analyze_file("source/tests/sample_test.py") 

    # 3. Construct the prompt for Gemini
    prompt = f"""
    Analyze the following QA Automation findings and provide refactoring suggestions:
    
    DEAD CODE FOUND: {dead_code_results}
    CODE SMELLS: {static_smells}

    Please format a report suggesting:
    - How to remove the dead code safely.
    - How to refactor the code smells into reusable components (e.g., Page Objects).
    - Identify any missing assertions or bad locator practices.
    """

    # 4. Get AI Insights
    print("Sending data to Gemini for analysis...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    # 5. Save to your reports folder
    os.makedirs("source/reports", exist_ok=True)
    with open("source/reports/report.md", "w") as f:
        f.write("# AI Test Maintenance Analysis Report\n\n")
        f.write(response.text)
    
    print("POC Successful: Report saved to source/reports/report.md")

if __name__ == "__main__":
    generate_ai_maintenance_report()