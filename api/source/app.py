from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from config.config_reader import ConfigReader
from config.db_config import Connection
from repository.data_collector import DataCollector

app = Flask(__name__)
CORS(app)

config_reader = ConfigReader()
app_config = config_reader.read_config("./config/config.yaml")


params = app_config.get('configuration_parameters', [])
def get_params(param_name):
    return next((param.get(param_name) for param in params if param_name in param), None)

debug =  get_params('debug')
database_host = get_params('database_host') 
database_port = get_params('database_port') 
database_name = get_params('database_name')
database_user = get_params('database_user')
database_password = get_params('database_password')
data_route = get_params('data_route')



def datetime_formatter(datetime_text):
    """
        Format the date from yyyy-mm-ddhhmmss to yyyy-mm-dd hh:mm:ss
    """
    try:
        datetime_text = f"{datetime_text[:10]} {datetime_text[10:12]}:{datetime_text[12:14]}:{datetime_text[14:]}"
        return datetime.strptime(datetime_text, "%Y-%m-%d %H:%M:%S")
    except Exception as error:
        print("Erro ao formatar data de YYYYMMDDHHMMSS para YYYY-MM-DD HH:MM:SS, ", error)
        return None



@app.route(data_route, methods=['GET'])
def get_data(initial_date, final_date):
    """
        Collects the particulate matter data in the reported period
    """
    initial_date = datetime_formatter(initial_date)
    final_date = datetime_formatter(final_date)

    # Checks if the dates were passed in the correct format
    if not initial_date or not final_date:
        return jsonify({"error": "Dates must be in the format YYYY-MM-DDHHMMSS"}), 400

    connection = Connection.db_connection(database_host, database_port, database_name, database_user, database_password)
    if connection:
        try:
            municipalities_data = DataCollector.select_data(connection, initial_date, final_date)
            return jsonify({"data": municipalities_data}), 200
        except Exception as error:
            print(error)
            return jsonify({"error": f"Erro ao transformar dados em JSON."}), 500
        finally:
            connection.close()


if __name__ == '__main__':
    app.run(debug=debug)
