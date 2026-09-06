import os
from crewai.tools import tool

@tool("Read Code File Content")
def read_target_file(file_path: str) -> str:
    """Useful to securely read the local contents of a code file designated for migration or infrastructure tracking."""
    if not os.path.exists(file_path):
        return f"Error: File target path '{file_path}' could not be located on the platform workspace."
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as error:
        return f"Failed to correctly load the specified source target file template. Reason: {str(error)}"
      
