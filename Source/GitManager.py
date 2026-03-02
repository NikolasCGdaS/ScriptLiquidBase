import subprocess
import os 

class GitManager:
    @staticmethod
    def prepare_repository(repo_path, branch_name):
        try:
            if not os.path.exists(repo_path):
                print(f"Error: The path {repo_path} does not exist.")
                return False
            print(f"------------------------------------")
            print(f"Accessing repository on: {repo_path}")

            print(f"Checkout to branch {branch_name}")
            subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)

            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error calling Git command: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error on GitManager: {e}")
            return False
        
    @staticmethod
    def commit_changes(repo_path, task_id):
        try:
            print(f"Adding changes to git index in: {repo_path}")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            status = subprocess.run(
                ["git", "status", "--porcelain"], 
                cwd=repo_path, 
                capture_output=True, 
                text=True
            )

            if not status.stdout.strip():
                print("No changes to commit (repository is clean).")
                return True
            
            message = f"US #{task_id}" 
            print(f"Committing changes: {message}")
            subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)

            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error during Git commit: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error on GitManager.commit_changes: {e}")
            return False