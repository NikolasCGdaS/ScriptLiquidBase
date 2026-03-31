import subprocess
import os
from unittest import case 

class GitManager:
    @staticmethod
    def setup_branch(environment, task_id, team_name):
        if environment == "homologation":
            return f"{team_name}/{task_id}"
        if environment == "production":
            return f"{team_name}/{task_id}_prod"
        return print("Error: Invalid environment specified for branch setup.")

    @staticmethod
    def prepare_repository(repo_path, branch_name, new_branch=0):
        try:
            if not os.path.exists(repo_path):
                print(f"Error: The path {repo_path} does not exist.")
                return False

            print(f"Accessing repository on: {repo_path}")

            if new_branch:
                subprocess.run(["git", "checkout", "-B", branch_name], cwd=repo_path, check=True)
            else:
                subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)                
            
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error calling Git command: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error on GitManager: {e}")
            return False
        except ValueError as e:
            print(f"Configuration error: {e}")
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
        
    @staticmethod
    def pull_changes(repo_path):
        try:
            print(f"Pulling latest changes in: {repo_path}")
            subprocess.run(["git", "pull"], cwd=repo_path, check=True)
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error during Git pull: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error on GitManager.pull_changes: {e}")
            return False
        
    @staticmethod
    def push_changes(repo_path, branch_name):
        try:
            print(f"Pushing changes to remote in: {repo_path}")
            subprocess.run(
                ["git", "push", "--set-upstream", "origin", branch_name], 
                cwd=repo_path, 
                check=True
            )
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"Error during Git push: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error on GitManager.push_changes: {e}")
            return False