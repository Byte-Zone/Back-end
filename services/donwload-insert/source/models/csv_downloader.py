import requests
import os

class CsvDownloader:

    def download_files(url_base, download_folder_path, connection):
        """
        Baixa os arquivos CSV do repositório GitHub e salva no diretório especificado.
        
        Args:
            url_base (str): URL da API do GitHub.
            download_folder_path (str): Caminho para salvar os arquivos.
            connection (object): Conexão com o banco de dados.
        
        Returns:
            list: Lista dos arquivos baixados.
        """
        os.makedirs(download_folder_path, exist_ok=True)

        response = requests.get(url_base)
        if response.status_code != 200:
            print("Erro ao acessar o repositório via API!")
            return []

        files = response.json()
        csv_files = [file for file in files if file["name"].endswith(".csv")]

        if not csv_files:
            print("Nenhum arquivo CSV encontrado!")
            return []

        downloaded_files = []

        for file in csv_files:
            file_name = file["name"]
            file_url = file["download_url"]

            print(f"Baixando {file_name}...")

            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                file_path = os.path.join(download_folder_path, file_name)
                with open(file_path, "wb") as f:
                    f.write(file_response.content)
                print(f"{file_name} salvo com sucesso!")
                downloaded_files.append(file_name)
            else:
                print(f"Erro ao baixar {file_name}")

        print("Todos os arquivos CSV foram baixados com sucesso!")
        return downloaded_files
