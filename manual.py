import subprocess
from rich.console import Console
import re

def is_valid_module_name(name):
    """
    Validate the Python module name.
    Args:
        name (str): The name of the Python module.
    Returns:
        bool: True if the name is valid, False otherwise.
    """
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

def get_pydoc(command):
    """
    Execute pydoc command to get documentation for the specified Python module.
    Args:
        command (str): The Python module to get documentation for.
    Returns:
        str: Documentation or error message.
    """
    if not is_valid_module_name(command):
        return "Invalid module name."

    try:
        result = subprocess.run(['python', '-m', 'pydoc', command], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Python executable not found."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def display_pydoc(command):
    """
    Display the documentation for the specified Python module using rich library.
    Args:
        command (str): The Python module to display documentation for.
    """
    doc_page = get_pydoc(command)
    if "Error" in doc_page:
        print(doc_page)
    else:
        console = Console()
        console.print(doc_page)

if __name__ == "__main__":
    try:
        while True:
            command = input("Enter the Python module to display the documentation for (or 'q' to quit): ").strip()
            if command.lower() == 'q':
                break
            elif command:
                display_pydoc(command)
            else:
                print("Please enter a valid Python module name.")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
