from pathlib import Path

class FileEditor:
    #Insere "BEGIN" e o "END" no arquivo 
    @staticmethod
    def script_formatting(file_path):
        
        path = Path(file_path)

        if not path.exists():
            print(f"Error: There is no archive {file_path} to edit.")
            return False
        
        try:
            content = path.read_text(encoding='utf-8')

            new_content = f"BEGIN\n\n{content}\n\nEND"

            path.write_text(new_content, encoding='utf-8')

            return True
        
        except Exception as e:
            print(f"Error editing archive: {e}")
            return False
        
    @staticmethod
    def verify_header(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [file.readline().strip().lower() for _ in range(3)]
                has_formatted = any("-- liquibase formatted sql" in l for l in lines)
                has_changeset = any("-- changeset" in l for l in lines)
                has_comment = any("-- comment us #" in l for l in lines)

                if has_formatted and has_changeset and has_comment:
                    return True
                
                return False
        except Exception as e:
            print(f"Error reading file for verification: {e}")
            return False