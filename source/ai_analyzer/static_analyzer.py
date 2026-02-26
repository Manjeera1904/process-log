import os
# 1. Change the import from OpenAI to Anthropic
from langchain_anthropic import ChatAnthropic 
from langchain_core.prompts import ChatPromptTemplate

# 2. Setup Claude (using Claude 3.5 Sonnet is usually best for code)
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", 
    temperature=0,
    # It will automatically look for ANTHROPIC_API_KEY in your env
)

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

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