import psycopg2

class Connection:
    def db_connection(database_host, database_port, database_name, database_user, database_password):
        """
            Connects to the PostgreSQL database
        """
        try:
            connection = psycopg2.connect(
                host=database_host,
                port=database_port,
                database=database_name,
                user=database_user,
                password=database_password
            )

            return connection
        except Exception as error:
            print(f"Erro ao conectar ao PostgreSQL: {error}")
            return None