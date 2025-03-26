import requests
import os
import re  # Importa regex para extrair números do nome do arquivo

class CsvDownloader:

    def download_files(url_base, download_folder_path, connection):
        """
        Baixa os arquivos CSV do repositório GitHub e salva no diretório especificado,
        adicionando um contador ao nome do arquivo para evitar sobrescritas.

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
                # Definir o nome base do arquivo sem extensão
                base_name = os.path.splitext(file_name)[0]  # Remove a extensão .csv

                # Obtém a lista de arquivos já existentes na pasta
                existing_files = os.listdir(download_folder_path)
                existing_numbers = []

                # Verifica se já existem arquivos com o mesmo nome base e extrai os números finais
                for existing_file in existing_files:
                    match = re.match(rf"{re.escape(base_name)}-(\d+)\.csv", existing_file)
                    if match:
                        existing_numbers.append(int(match.group(1)))  # Adiciona o número extraído

                # Define o próximo número disponível (incrementa a partir do maior encontrado)
                next_number = max(existing_numbers) + 1 if existing_numbers else 1
                new_file_name = f"{base_name}-{next_number}.csv"

                # Caminho completo do arquivo
                file_path = os.path.join(download_folder_path, new_file_name)

                # Salvar o arquivo baixado
                with open(file_path, "wb") as f:
                    f.write(file_response.content)

                print(f"{new_file_name} baixado com sucesso!")
                downloaded_files.append(new_file_name)
            else:
                print(f"Erro ao baixar {file_name}")

        print("Todos os arquivos CSV foram baixados com sucesso!")
        return downloaded_files
