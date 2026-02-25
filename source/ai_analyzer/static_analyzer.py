import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    # Specialized Prompt for Maintenance Requirements
    prompt = ChatPromptTemplate.from_template("""
    Act as a Senior SDET. Analyze the following code from {file_path}.
    Identify only the following:
    1. Hardcoded locators (e.g., long XPaths) or sensitive data.
    2. Weak validations (e.g., missing assertions or using 'sleep' instead of waits).
    3. Naming convention issues.
    
    If no issues are found, return nothing.
    Code:
    {code}
    """)
    
    chain = prompt | llm
    response = chain.invoke({"file_path": file_path, "code": code_content})
    
    # Return as a list for main.py to iterate
    suggestions = response.content.strip().split('\n')
    return [s for s in suggestions if s.strip()]