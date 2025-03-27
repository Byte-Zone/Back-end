from flask import Flask, request, render_template
import requests
from config.config_reader import ConfigReader


app = Flask(__name__)

config_reader = ConfigReader()
app_config = config_reader.read_config("./config/config.yaml")

params = app_config.get('configuration_parameters', [])
def get_params(param_name):
    return next((param.get(param_name) for param in params if param_name in param), None)

debug =  get_params('debug')
api_data_route = get_params('api_data_route')



@app.route('/', methods=['GET'])
def get_data():

    initial_date = request.args.get('initial_date')
    final_date = request.args.get('final_date')

    if not initial_date or not final_date:
        return render_template('index.html', alldata=[])


    # Initiating request to the API
    api_url = api_data_route.replace("<initial_date>", f"{initial_date}").replace("<final_date>", f"{final_date}")
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        data = []


    # Formatting dates
    def format_datetime(date_str): 
        return f"{date_str[:10]} {date_str[10:12]}:{date_str[12:14]}:{date_str[14:16]}"

    initial_date = format_datetime(initial_date)
    final_date = format_datetime(final_date)
    
    return render_template('index.html', alldata=data, initial_date=initial_date, final_date=final_date)


if __name__ == '__main__':
    app.run(debug=debug)
