from langchain_core.tools import tool
from fastapi import HTTPException
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.services.config import groq_model

@tool
async def understand_files_codebase(
    path: str
) -> dict:
    """
    - Analyzes all source code files within a specified directory to understand their programming language, structure, and logic.
    - Use this tool when you need a comprehensive overview of a codebase or directory contents.
    - Input should be the directory path. Returns a dictionary mapping each file name to its detected language and a concise 
    explanation of its purpose and key functions.
    """
    try:
        prompt = PromptTemplate(
            template="""
                You are a code analysis assistant. The user will provide the contents of a source code file. Analyze it thoroughly 
                and respond ONLY with a valid JSON object — no explanation, no markdown, no preamble.
                
                The JSON must follow this exact structure:
                {{
                    // the programming language detected (e.g. "Python", "JavaScript")
                    "lang": string,
                    /*a clear, concise explanation of what the code does, its structure, key logic, and any notable patterns or 
                    dependencies*/
                    "content": string
                }}

                Rules:
                - Detect the language from syntax and file structure, not just file extension.
                - The content explanation should cover: overall purpose, key functions/classes, important logic flows, and any 
                external dependencies or side effects. If the file contains multiple languages (e.g. HTML with embedded JS), set lang 
                to the dominant one and note the others in content. Never include anything outside the JSON object in your response.

                CONTENT in File:
                {file_data}
            """,
            input_variables=['file_data']
        )

        chain = prompt | groq_model | JsonOutputParser()

        import os
        file_explaination = {}

        for root, dirs, files in os.walk(path, topdown=True):
            for file in files:
                content = open(os.path.join(root, file), "r", encoding="utf-8").read()
                response = await chain.ainvoke({
                    "file_data": content
                })

                file_explaination[file] = response

        return file_explaination

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occurred while agent tried to understand codebase.")