from langchain_core.tools import tool
from fastapi import HTTPException

@tool
async def map_codebase(
    codebase: dict
) -> str:
    """
    Generates a comprehensive map of the codebase structure and relationships.

    Takes a dictionary mapping filenames to their descriptions and returns:
    - Directory Tree: Reconstructed folder structure grouping related files
    - Dependency Map: Lists each file's dependencies in format: filename → [dep1, dep2]
    - Layer Map: Assigns each file to a layer (UI, API, Business Logic, Data, Config, Utility, Test)
    - Core Path: The main execution path from entry point to output

    Use this tool when you need to understand the overall architecture and file relationships in a codebase.
    """
    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from src.services.config import gemini_model

        prompt = PromptTemplate(
            template="""
                You are an expert software architect. You will be given a dictionary where keys are filenames and values are their 
                descriptions. Generate a visual codebase map in the following format:

                Directory Tree — Reconstruct the likely folder structure grouping related files together.
                Dependency Map — List each file and which other files it depends on or connects to, in the format:
                filename → [file1, file2, ...]
                Layer Map — Assign every file to one layer:
                UI | API | Business Logic | Data | Config | Utility | Test
                Core Path — Trace the single most important execution path from entry point to output, listing files in order.

                Here is the codebase:
                {codebase_data}
                
                Return the output strictly as a JSON object with the following structure. No explanation, no markdown, no code 
                fences — raw JSON only.
                
                {{
                    "directory_tree": {{
                        "folder_name": ["file1", "file2"],
                        ...
                    }},
                    "dependency_map": {{
                        "filename": ["dep1", "dep2"],
                        ...
                    }},
                    "layer_map": {{
                        "filename": string,
                        ...
                    }},
                    "core_path": ["file1", "file2", "file3"]
                }}
            """,
            input_variables=['codebase_data']
        )

        chain = prompt | gemini_model | StrOutputParser()
        response = await chain.ainvoke({
            "codebase_data": codebase
        })

        return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occured while mapping the codebase.")

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
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        from src.services.config import groq_model

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
                external dependencies or side effects. If the file contains multiple languages (e.g. HTML with embedded JS), set 
                language to the dominant one and note the others in content. Never include anything outside the JSON object in your 
                response.

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
                file_path = os.path.join(root, file)
                content = open(file_path, "r", encoding="utf-8").read()
                response = await chain.ainvoke({
                    "file_data": content
                })

                file_explaination[file_path] = response

        return file_explaination

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occurred while agent tried to understand codebase.")

@tool
async def locate_errors(
    path: str
):
    """
    Performs static analysis to detect errors in code files within a directory.

    Takes a directory path and scans all files for:
    - Syntax errors
    - Logical errors
    - Runtime risks
    - Security vulnerabilities
    - Bad practices

    Returns a dictionary mapping file paths to error reports, where each report contains:
    - total_errors: Count of issues found
    - errors: Array of detailed error objects with id, type, severity, line, description, impact, and fix
    - summary: One-sentence assessment of file health

    Use this tool when you need to identify bugs, security issues, or code quality problems in a codebase.
    """
    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        from src.services.config import groq_model

        prompt = PromptTemplate(
            template="""
                You are an expert code reviewer and static analysis agent.
                You will be given a file's name and its contents. Your job is to detect all errors present in the file — including 
                syntax errors, logical errors, runtime risks, bad practices, and security vulnerabilities. Analyze the file thoroughly 
                and respond strictly as a JSON object. No explanation, no markdown, no code fences — raw JSON only.
                
                Use this structure:
                
                {{
                    "total_errors": 3,
                    "errors": [
                        {{
                            "id": 1,
                            "type": "syntax | logical | runtime | security | bad_practice",
                            "severity": "critical | high | medium | low",
                            "line": 42,
                            "description": "What the error is",
                            "impact": "What will go wrong if this is not fixed",
                            "fix": "How to fix it"
                        }}
                    ],
                    "summary": "One sentence describing the overall health of the file"
                }}
                
                Rules:

                If no errors are found, return "errors": [] and "total_errors": 0
                line should be the exact line number where the error occurs, or null if not locatable
                severity must reflect real impact — do not inflate or downplay
                Do not suggest stylistic preferences unless they introduce a real risk
                One error object per distinct issue — do not bundle multiple errors together

                Contents:
                {file_contents}
            """,
            input_variables=['file_content']
        )

        chain = prompt | groq_model | JsonOutputParser()

        import os
        errors = {}

        for root, dirs, files in os.walk(path, topdown=True):
            for file in files:
                file_path = os.path.join(root, file)
                content = open(file_path, "r", encoding="utf-8").read()
                response = await chain.ainvoke({
                    "file_content": content
                })

                errors[file_path] = response

        return errors

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error {e} occurred while locating errors in codebase.")