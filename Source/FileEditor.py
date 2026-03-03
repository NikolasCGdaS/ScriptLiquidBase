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