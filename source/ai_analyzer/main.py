import os
from google import genai
# Import your existing logic from your other files
from dead_code_detector import detect_dead_code
from static_analyzer import run_static_analysis

client = genai.Client(api_key="AIzaSyDd1v3JL25BSDFgom5lVm1cUbtVopLR2Ik")

def generate_ai_maintenance_report():
    # 1. Get data from your existing python scripts
    dead_code_results = detect_dead_code()
    static_smells = run_static_analysis()

    # 2. Construct the prompt for Gemini
    prompt = f"""
    Analyze the following QA Automation findings and provide refactoring suggestions:
    
    DEAD CODE FOUND: {dead_code_results}
    CODE SMELLS: {static_smells}

    Please format a report suggesting:
    - How to remove the dead code safely.
    - How to refactor the code smells into reusable components.
    """

    # 3. Get AI Insights
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    # 4. Save to your reports folder (as seen in your screenshot)
    with open("source/reports/report.md", "w") as f:
        f.write(response.text)

if __name__ == "__main__":
    generate_ai_maintenance_report()