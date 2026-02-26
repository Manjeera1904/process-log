import os
# 1. Updated imports for Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 2. Setup Gemini 
# It will automatically look for GOOGLE_API_KEY in your env
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0,
)

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # The prompt remains the same—LangChain makes this easy!
    prompt = ChatPromptTemplate.from_template("""
    Review this test code for:
    - Hardcoded locators (XPaths/CSS)
    - Weak waits (Thread.sleep/time.sleep)
    - Missing assertions
    File: {path}
    Code: {code}
    Return a bulleted list of issues. If none, return 'No issues'.
    """)
    
    chain = prompt | llm
    res = chain.invoke({"path": file_path, "code": code})
    return res.content.strip()