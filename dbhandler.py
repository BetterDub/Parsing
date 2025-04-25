import psycopg2

class DBHandler:
    def __init__(self, options : dict) -> None:
        try:
            # Connect to PostgreSQL
            self.connection = psycopg2.connect(
                dbname = options["DB_NAME"],
                user = options["DB_USER"],
                password = options["DB_PASSWORD"],
                host = options["DB_HOST"],
                port = options["DB_PORT"]
            )
            print("Connection to PostgreSQL successful")
            
            self.cursor = self.connection.cursor()
            # cursor.execute("SELECT version();")
            # db_version = cursor.fetchone()
            # print("Database version:", db_version)
        except Exception as e:
            print("Error while connecting to PostgreSQL:", e)

        # finally:
        #     if 'connection' in locals() and self.connection:
        #         #self.cursor.close()
        #         #connection.close()
        #         print("PostgreSQL connection closed.")

    # DANGEROUS (dealut commit = true)
    def executeQuery(self, query : str, commit : bool = True) -> None:
        self.cursor.execute(query)
        if commit:
            self.connection.commit()

    # Fetches the all rows of a response
    def fetch(self) -> list:
        return self.cursor.fetchall()

    # Just gonna leave it here:
    # If you encounter "cannot run inside transaction block" error
    # Then you need to execute 'SET AUTOCOMMIT = ON' in live-mode
    # In case this doesn't work check this out: 
    # https://stackoverflow.com/questions/26482777/create-database-cannot-run-inside-a-transaction-block

    # Imitates DBMS (is proxy-DBMS??...)
    def liveMode(self):
        query = 'idle'
        while query != 'exit':
            query = input()
            try:
                self.executeQuery(query=query)
                print(self.fetch())
            except Exception as e:
                print("DBHandler live-mode error: ", e)

    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print("Failed to close PostreSQL connection: ", e)