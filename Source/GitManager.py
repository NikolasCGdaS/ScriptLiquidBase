import subprocess
import os
from unittest import case 

class GitManager:
    @staticmethod
    def prepare_repository(repo_path, branch_name, branch_type, team_name=None):
        try:
            if not os.path.exists(repo_path):
                print(f"Error: The path {repo_path} does not exist.")
                return False

            print(f"Accessing repository on: {repo_path}")

            match branch_type:
                case "homologation" | "production":
                    print(f"Checkout to branch {branch_name}")
                    subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
                    if not GitManager.pull_changes(repo_path):
                        return False

                case "new_homologation" | "new_production":
                    if not team_name:
                        raise ValueError(f"O parâmetro 'team_name' é obrigatório para '{branch_type}'")
                    
                    suffix = "_prod" if branch_type == "new_production" else ""
                    full_name = f"{team_name}/{branch_name}{suffix}"
                    
                    print(f"Creating branch {full_name} based on {branch_type.split('_')[1]}")
                    subprocess.run(["git", "checkout", "-b", full_name], cwd=repo_path, check=True)
                    
                case _:
                    raise ValueError(f"Invalid branch type '{branch_type}' provided.")
                
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
    def push_changes(repo_path, task_id, team_name):
        try:
            full_branch = f"{team_name}/{task_id}"
            print(f"Pushing changes to remote in: {repo_path}")
            subprocess.run(
                ["git", "push", "--set-upstream", "origin", full_branch], 
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