import os
import sys
# Ensures the script finds local imports in the same folder
sys.path.append(os.path.dirname(__file__))

from dead_code_detector import detect_dead_code
from static_analyzer import analyze_file

def main():
    # 1. Run Dead Code Detection
    dead_code = detect_dead_code()
    
    # 2. Run Static Analysis on a sample test file
    # Change 'sample_test.py' to a file that exists in your 'source/web' folder
    test_file = "source/web/sample_test.py" 
    smells = analyze_file(test_file)

    # 3. Final Report generation using Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    from google import genai
    client = genai.Client(api_key=api_key)

    final_prompt = f"""
    Format a QA Maintenance Report based on these findings:
    
    UNLINKED/DEAD FILES:
    {dead_code}
    
    CODE SMELLS IN {test_file}:
    {smells}
    
    Provide clear refactoring steps.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=final_prompt
    )

    # 4. Save the report to the path shown in your screenshot
    report_path = "source/reports/report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(response.text)
    
    print(f"✅ POC Complete! Report generated at {report_path}")

if __name__ == "__main__":
    main()