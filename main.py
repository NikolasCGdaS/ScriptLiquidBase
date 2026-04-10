import os
from pathlib import Path
from dotenv import load_dotenv
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
    proj_path = os.getenv("PROJECT_PATH")
    team = os.getenv("TEAM_NAME")
    homol_branch = os.getenv("HOMOL_BRANCH")
    prod_branch = os.getenv("PROD_BRANCH")
    download_folder = Path(__file__).parent / "Downloads"

    print("=== Azure DevOps Task Downloader ===")

    if not all([pat, org, project, proj_path, homol_branch, prod_branch]):
        print("Error: There are missing configuration on .env")
        return

    task_id = input("Type the task ID: ").strip()

    if not task_id.isdigit():
        print("Error: Task ID must contain only numbers.")
        return
    
    team_lower = team.lower()

    new_branch_from_prod = GitManager.setup_branch("production", task_id, team_lower)
    new_branch_from_homol = GitManager.setup_branch("homologation", task_id, team_lower)
    
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
        print(f"Script formatting completed for {len(files_list)} file(s).")

    else:
        print("No .sql files found to process.")
        return False
    
    print("-"*30)
    
    GitManager.prepare_repository(proj_path, homol_branch)

    GitManager.pull_changes(proj_path)

    print("-"*30)

    GitManager.prepare_repository(proj_path, new_branch_from_homol, 1)

    print("-"*30)

    script_destination = MoveScript.script_destination(proj_path, team)

    MoveScript.move_to(download_folder, script_destination, task_id)

    print("-"*30)

    GitManager.commit_changes(proj_path, task_id)

    print("-"*30)

    if not GitManager.push_changes(proj_path, new_branch_from_homol):
        print("Failed to push changes to remote repository.")
        return
    
    print("\n" + "[]" * 20 + "\n")
    print("Script sent to Azure DevOps Successfully! Please execute the Pipeline!")

    confirm = input("Has the pipeline been executed successfully? (y/n): ").strip().lower()

    if confirm == 'y':
        GitManager.pull_changes(proj_path)

        all_ok = True

        for file in script_destination.iterdir():
            if FileEditor.verify_header(file):
                print(f"{file.name}: Header verified.")
            else:
                print(f"{file.name}: Missing or invalid header at {file}")
                all_ok = False
        
        if all_ok: 
            print("All files have the required header. Process completed successfully!")
            MoveScript.move_to(script_destination, download_folder, task_id)

            
            
            GitManager.prepare_repository(proj_path, prod_branch)
            GitManager.pull_changes(proj_path)

            print("\n" + "[]" * 20 + "\n")

            GitManager.prepare_repository(proj_path, new_branch_from_prod, 1)

            print("\n" + "[]" * 20 + "\n")

            MoveScript.move_to(download_folder, script_destination, task_id)

            

            GitManager.commit_changes(proj_path, task_id)
            GitManager.push_changes(proj_path, new_branch_from_prod)
        
    else:
        print("Please correct the error in the pipeline and try again.")

    print("-"*30)    
    print("Process finished.")
                

if __name__ == "__main__":
    executar_processo()