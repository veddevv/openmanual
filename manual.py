import subprocess
from rich.console import Console

def get_pydoc(command):
    try:
        result = subprocess.run(['python', '-m', 'pydoc', command], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def display_pydoc(command):
    doc_page = get_pydoc(command)
    if "Error" in doc_page:
        print(doc_page)
    else:
        console = Console()
        console.print(doc_page)

if __name__ == "__main__":
    while True:
        command = input("Enter the Python module to display the documentation for (or 'q' to quit): ")
        if command.lower() == 'q':
            break
        display_pydoc(command)