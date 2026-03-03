import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from Source.DownloadScript import DownloadScript
from Source.FileEditor import FileEditor
from Source.GitManager import GitManager
from Source.MoveScript import MoveScript

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def executar_processo():
    # Credenciais necessárias
    project = os.getenv("AZURE_PROJECT")
    pat = os.getenv("AZURE_PAT")
    org = os.getenv("AZURE_ORG")
    dest_path = os.getenv("PROJECT_PATH")
    team = os.getenv("TEAM_NAME")
    homol_branch = os.getenv("HOMOL_BRANCH")
    prod_branch = os.getenv("PROD_BRANCH")

    print("=== Azure DevOps Task Downloader ===")

    if not all([pat, org, project, dest_path, homol_branch, prod_branch]):
        print("Error: There are missing configuration on .env")
        return

    task_id = input("Type the task ID: ").strip()

    if not task_id.isdigit():
        print("Error: Task ID must contain only numbers.")
        return
    
    print("-"*30)

    # Inicializa a classe DownloadScript
    download_script = DownloadScript(pat=pat, org=org)

    files_list = download_script.download_task_script(
        project=project, 
        task_id=task_id
    )

    print("-"*30)

    if files_list:
        for file in files_list:
            FileEditor.script_formatting(file)
        print(f"Script formatting completed for {len(files_list)} files.")

    else:
        print("No .sql files found to process.")
        return False
    
    print("-"*30)
    
    GitManager.prepare_repository(dest_path, homol_branch, "homologation")

    print("-"*30)

    GitManager.prepare_repository(dest_path, task_id, "new_homologation", "pa")

    print("-"*30)

    moved_files = MoveScript.move_to(
        source_files=files_list, 
        destination_path=dest_path,
        team_name=team
        )
    
    if moved_files:
        print(f"Successfully moved {len(moved_files)} files to {dest_path}/{team}/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}")
    else:
        print("Failed to move files.")

if __name__ == "__main__":
    executar_processo()