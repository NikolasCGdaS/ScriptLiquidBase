import shutil
import os
from pathlib import Path
from datetime import datetime

class MoveScript:
    @staticmethod
    def move_to(source_files, destination_path, team_name):

        files = []

        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        path_base = Path(destination_path) / "sql"
        path_team = path_base / team_name
        path_final = path_team / year / month

        try:

            if not path_team.exists():
                print(f"Error: Team directory '{team_name}' not found in {path_base}")
                return[]

            if not path_final.exists():
                print(f"Creating directory structure: {datetime.now().strftime('%Y/%m')}")
                path_final.mkdir(parents=True, exist_ok=True)

            for file_path in source_files:
                src = Path(file_path)

                if src.exists():
                    destination = path_final/src.name

                    print(f"Moving: {src.name} to {path_final}")

                    shutil.move(str(src), str(destination))
                    files.append(str(destination))
                else:
                    print(f"Warning: File not found: {file_path}")

            print(f"Succesfully moved {len(files)} files.")
            return files
        
        except Exception as e:
            print(f"Unexpected error while moving files: {e}")
            return []