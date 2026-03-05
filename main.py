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

    print("=== Azure DevOps Task Downloader ===")

    if not all([pat, org, project, proj_path, homol_branch, prod_branch]):
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
        print(f"Script formatting completed for {len(files_list)} file(s).")

    else:
        print("No .sql files found to process.")
        return False
    
    print("-"*30)
    
    GitManager.prepare_repository(proj_path, homol_branch, "homologation")

    print("-"*30)

    GitManager.prepare_repository(proj_path, task_id, "new_homologation", "pa")

    print("-"*30)

    script_destination = MoveScript.script_destination(proj_path, team)

    moved_files = []

    for file in files_list:
        result = MoveScript.move_to(
            file_path=file, 
            destination_path=script_destination,
            task_id=task_id
        )
        if result:
            moved_files.append(result)
    
    if moved_files:
        print(f"Successfully moved {len(moved_files)} file(s) to {script_destination}")
    else:
        print("Failed to move files.")

    GitManager.commit_changes(proj_path, task_id)

    if not GitManager.push_changes(proj_path, task_id, "pa"):
        print("Failed to push changes to remote repository.")
        return
    
    print("\n" + "()" * 20)
    print("Script sent to Azure DevOps Successfully! Please execute the Pipeline!")

    confirm = input("Has the pipeline been executed successfully? (y/n): ").strip().lower()

    if confirm == 'y':
        GitManager.pull_changes(proj_path)

        all_ok = True

        for file_path in moved_files:
            if FileEditor.verify_header(file_path):
                print(f"{Path(file_path).name}: Header verified.")
            else:
                print(f"{Path(file_path).name}: Missing or invalid header at {file_path}")
                all_ok = False
        
        if all_ok:
            print("All files have the required header. Process completed successfully!")
            for f_path in moved_files:
                res= MoveScript.move_to(
                    f_path, 
                    download_script.download_folder,
                    task_id
                )
                if res:
                    moved_files.append(result)
            
            GitManager.prepare_repository(proj_path, prod_branch, "production")
            GitManager.pull_changes(proj_path)

            GitManager.prepare_repository(proj_path, task_id, "new_production", "pa")

            for f_path in moved_files:
                MoveScript.move_to(f_path, script_destination, task_id)

            GitManager.commit_changes(proj_path, task_id)
            GitManager.push_changes(proj_path, task_id, "pa")
        
    else:
        print("Please correct the error in the pipeline and try again.")

    print("-"*30)    
    print("Process finished.")
                

if __name__ == "__main__":
    executar_processo()