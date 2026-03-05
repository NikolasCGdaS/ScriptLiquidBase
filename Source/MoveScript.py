import shutil
from pathlib import Path
from datetime import datetime

class MoveScript:
    @staticmethod
    def script_destination(destination_path, team_name):
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        path_base = Path(destination_path) / "sql"
        path_team = path_base / team_name
        path_final = path_team / year / month

        try:
            if not path_team.exists():
                print(f"Error: Team directory '{team_name}' not found in {path_base}")
                return None

            if not path_final.exists():
                print(f"Creating directory structure: {datetime.now().strftime('%Y/%m')}")
                path_final.mkdir(parents=True, exist_ok=True)
            
            return path_final
        
        except Exception as e:
            print(f"Unexpected error while : {e}")
            return None


    @staticmethod
    def move_to(file_path, destination_path, task_id):

        task_id_str = str(task_id)

        try:
            src = Path(file_path)
            dest_dir = Path(destination_path)

            if src.exists() and task_id_str in src.name:
                destination = dest_dir/src.name

                print(f"Moving: {src.name} -> {dest_dir}")
                shutil.move(str(src), str(destination))
                return str(destination)
            
            if not src.exists():
                print(f"⚠️ Warning: File not found: {file_path}")

            elif task_id_str not in src.name:
                print(f"⏭️ Skipping: '{src.name}' (ID {task_id_str} not found in name)")
            
            return None
        
        except Exception as e:
            print(f"Unexpected error while moving file {file_path}: {e}")
            return []