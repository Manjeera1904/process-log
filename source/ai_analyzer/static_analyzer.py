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
        Review this automation code for the following:
        1. Code Smells: Hardcoded locators, time.sleep, missing assertions, indexing in locators.
        2. Refactoring: Suggest where logic can be moved to a Page Object or Shared Utility.
        3. Readability: Suggest better naming if methods are confusing.
        4. Maintenance: Identify overly complex or lengthy test methods.

        File: {path}
        Code: {code}

        Return a bulleted list of improvement areas. If the code is perfect, return 'No issues'.
        """)
    chain = prompt | llm
    res = chain.invoke({"path": file_path, "code": code})
    return res.content.strip()