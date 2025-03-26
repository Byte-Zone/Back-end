from datetime import datetime

class DataCollector:
    def select_data(connection, initial_date, final_date):
        """
            Collects data from the database in the reported period
        """
        cursor = connection.cursor()
        try:
            query = f"""
                        SELECT municipio, estado, media_pm2_5, data, data_insercao
                        FROM bdc.csv_infos
                        WHERE data_insercao BETWEEN %s AND %s;
                    """
            cursor.execute(query, (initial_date, final_date))
            results = cursor.fetchall()
            
            results_list = []
            for row in results:
                results_list.append({
                    "municipio": row[0],
                    "estado": row[1],
                    "media_pm2_5": row[2],
                    "data": row[3].strftime('%Y-%m-%d %H:%M:%S'),
                    "data_insercao": row[4].strftime('%Y-%m-%d %H:%M:%S')
                })

            return results_list
        except Exception as error:
            print(f"Erro ao executar a consulta: {error}")
        finally:
            if cursor:
                cursor.close()