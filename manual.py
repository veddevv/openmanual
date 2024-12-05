import subprocess
from rich.console import Console
import re
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_module_name(name: str) -> bool:
    """
    Validate the Python module name.

    Args:
        name (str): The name of the Python module.
    Returns:
        bool: True if the name is valid, False otherwise.
    """
    return re.fullmatch(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

def get_pydoc(command: str) -> str:
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

def display_pydoc(command: str) -> None:
    """
    Display the documentation for the specified Python module using rich library.

    Args:
        command (str): The Python module to display documentation for.
    """
    console = Console()
    doc_page = get_pydoc(command)
    if "Error" in doc_page:
        console.print(doc_page, style="bold red")
    else:
        console.print(doc_page)

def main() -> None:
    """
    Main function to handle user input and display documentation.
    """
    console = Console()
    try:
        while True:
            command = console.input("Enter the Python module to display the documentation for (or 'q' to quit): ").strip()
            if command.lower() == 'q':
                console.print("Exiting...", style="bold yellow")
                sys.exit(0)
            elif command:
                display_pydoc(command)
            else:
                console.print("Please enter a valid Python module name.", style="bold yellow")
    except KeyboardInterrupt:
        console.print("\nExiting...", style="bold yellow")
        sys.exit(0)
    except Exception as e:
        console.print(f"An unexpected error occurred: {str(e)}", style="bold red")
        sys.exit(1)

if __name__ == "__main__":
    main()
