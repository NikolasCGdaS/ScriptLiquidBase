import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

# Classe para baixar o script da tarefa do Azure DevOps
class DownloadScript:
    # Inicialização da classe com as credenciais e organização
    def __init__(self, pat, org):
        self.pat = pat
        self.org = org
        self.base_url = f"https://dev.azure.com/{org}"
        self.auth = HTTPBasicAuth('', self.pat)
        self.download_folder = Path(__file__).parent.parent / "Downloads"
        
    # Método para baixar o script da tarefa
    def download_task_script(self, project, task_id):
        url_task = f"{self.base_url}/{project}/_apis/wit/workitems/{task_id}?$expand=relations&api-version=7.1"
        downloaded_files = []
        
        try:
            response = requests.get(url_task, auth=self.auth)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            data = response.json()

            relations = data.get('relations', [])

            valid_attachments = []
            for rel in relations:
                if rel.get('rel') == 'AttachedFile':
                    name = rel.get('attributes', {}).get('name', '').lower()
                    if name.endswith('.sql'):
                        valid_attachments.append(rel)
            
            total_files = len(valid_attachments)

            for index, rel in enumerate(valid_attachments, start=1):
                attachment_url = rel.get('url')
                
                # Se houver mais de um, adiciona o sufixo. Se for um só, mantém o padrão.
                if total_files > 1:
                    file_name = f"US#{task_id}_{index}.sql"
                else:
                    file_name = f"US#{task_id}.sql"

                full_path = self.download_folder / file_name
                
                print(f"Downloading: {file_name}")
                file_response = requests.get(attachment_url, auth=self.auth)
                file_response.raise_for_status()

                with open(full_path, 'wb') as f:
                    f.write(file_response.content)
                
                downloaded_files.append(str(full_path.absolute()))

            return downloaded_files
           
        except Exception as e:
            print(f"Error: {e}")
            return []
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Error: invalid Token.")
            elif e.response.status_code == 404:
                print("Error: Task or Project not found.")
            else:
                print(f"HTTP Error: {e}")