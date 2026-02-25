import os
from langchain_openai import ChatOpenAI
# UPDATED IMPORT PATH
from langchain_core.prompts import ChatPromptTemplate 

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # The logic remains the same, only the source of ChatPromptTemplate changed
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