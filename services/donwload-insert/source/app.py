import os
import pandas as pd
from datetime import datetime  # Para capturar a data e hora local
from config.config_reader import ConfigReader
from models.csv_downloader import CsvDownloader
from repository.data import Data 
from config.db_config import Connection

# Lendo os parâmetros do YAML
config_reader = ConfigReader()
app_config = config_reader.read_config("./config/config.yaml")
params = app_config.get('configuration_parameters', [])

def get_params(param_name):
    return next((param.get(param_name) for param in params if param_name in param), None)  

def read_csv(file_path):
    """
    Lê os dados do arquivo CSV usando pandas e os formata para inserção no banco.
    """
    try:
        # Lê o CSV com pandas
        df = pd.read_csv(file_path)

        # Garantir que as colunas têm os nomes esperados
        if not all(col in df.columns for col in ['estado', 'municipio', 'media_pm2_5', 'data']):
            raise ValueError("O arquivo CSV não possui as colunas esperadas: estado, municipio, media_pm2_5, data.")

        # Convertendo a coluna 'media_pm2_5' para float e 'data' para datetime (se necessário)
        df['media_pm2_5'] = pd.to_numeric(df['media_pm2_5'], errors='coerce')  # Converte para float, 'coerce' transforma erros em NaN
        df['data'] = pd.to_datetime(df['data'], errors='coerce')  # Converte para datetime, 'coerce' trata erros

        # Filtrando as linhas que podem ter valores inválidos após conversão
        df = df.dropna(subset=['media_pm2_5', 'data'])

        # Adiciona a coluna de data de inserção (timestamp local)
        current_timestamp = datetime.now()  # Data e hora local
        df['data_insercao'] = current_timestamp

        # Formatar os dados para a inserção
        data = [(row['estado'], row['municipio'], row['media_pm2_5'], row['data'], row['data_insercao']) for _, row in df.iterrows()]

        return data
    
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return []

def main():
    url_base = get_params('url_base')
    download_folder_path = get_params('download_folder_path')
    database_host = get_params('database_host')
    database_name = get_params('database_name')
    database_port = get_params('database_port')
    database_user = get_params('database_user')
    database_password = get_params('database_password')
    
    connection = Connection.db_connection(database_host, database_port, database_name, database_user, database_password)
    if connection:
        downloaded_files = CsvDownloader.download_files(url_base, download_folder_path, connection)
        
        if downloaded_files:
            for file_name in downloaded_files:
                file_path = os.path.join(download_folder_path, file_name)

                # Ler e inserir os dados no banco
                csv_data = read_csv(file_path)
                if csv_data:
                    insert_result = Data.insert_csv(csv_data, connection)
                    print(insert_result["message"])

        connection.close()
    else:
        print("Não foi possível conectar-se ao banco de dados.")           

if __name__ == "__main__":
    main()
