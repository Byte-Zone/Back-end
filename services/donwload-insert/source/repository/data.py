import psycopg2

class Data:
    
    def insert_csv(data, connection):
        """
        Insere os dados do CSV na tabela bdc.csv_infos no banco de dados.
        """
        try:
            with connection.cursor() as cursor:
                # Criar schema e tabela apenas uma vez
                cursor.execute("CREATE SCHEMA IF NOT EXISTS bdc;")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bdc.csv_infos (
                        id SERIAL PRIMARY KEY,
                        estado CHARACTER VARYING(100),
                        municipio CHARACTER VARYING(100) NOT NULL,
                        media_pm2_5 FLOAT,
                        data TIMESTAMP NOT NULL
                    );
                """)
                connection.commit()

                insert_query = """
                    INSERT INTO bdc.csv_infos (estado, municipio, media_pm2_5, data) 
                    VALUES (%s, %s, %s, %s);
                """

                # 🔥 Certifique-se de que os dados seguem a ordem correta (estado, município, media_pm2_5, data)
                formatted_data = [(row[0], row[1], float(row[2]) if row[2] else None, row[3]) for row in data]

                # 🔥 Executa a inserção em lote
                cursor.executemany(insert_query, formatted_data)
                connection.commit()

                return {"status": "ok", "message": "Todos os dados foram inseridos com sucesso!"}
        
        except psycopg2.Error as error:
            connection.rollback()  # Reverte mudanças no caso de erro
            return {"status": "error", "message": f"Erro ao inserir dados no PostgreSQL: {error}"}
