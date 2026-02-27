import os
from pathlib import Path
from dotenv import load_dotenv
from Source.DownloadScript import DownloadScript
from Source.FileEditor import FileEditor

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def executar_processo():
    # Credenciais necessárias
    project = os.getenv("AZURE_PROJECT")
    pat = os.getenv("AZURE_PAT")
    org = os.getenv("AZURE_ORG")

    print("=== Azure DevOps Task Downloader ===")

    if not all([pat, org, project]):
        print("Error: There are missing configuration on .env")
        return

    task_id = input("Type the task ID: ").strip()

    if not task_id.isdigit():
        print("Error: Task ID must contain only numbers.")
        return

    # Inicializa a classe DownloadScript
    download_script = DownloadScript(pat=pat, org=org)

    print(f"Searching for task #{task_id}...")

    files_list = download_script.download_task_script(
        project=project, 
        task_id=task_id
    )

    if files_list:
        for file in files_list:
            FileEditor.script_formatting(file)
            print(f"Processed: {Path(file).absolute()}")
    
    else:
        print("No .sql files found to process.")

if __name__ == "__main__":
    executar_processo()