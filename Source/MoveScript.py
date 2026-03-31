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
    def move_to(origin_folder, destination_folder, task_id):

        task_id_str = str(task_id)
        origin = Path(origin_folder)
        destination = Path(destination_folder)

        for item in origin.iterdir():
            if item.is_file() and str(task_id) in item.name:
                try:
                    shutil.move(str(item), str(destination / item.name))
                    print(f"Sucess moving {item.name} to {destination}")
                except Exception as e:
                    print(f"Erro ao mover {item.name}: {e}")