from sqlalchemy import create_engine

class MySQLDatabase:
    def __init__(self, username, password, hostname, port, database_name):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database_name = database_name
        self.engine = None

    def connect(self):
        if not self.engine:
            connection_string = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_name}"
            self.engine = create_engine(connection_string)
            print("Connected to MySQL database.")

    def execute_query(self, query):
        if not self.engine:
            self.connect()
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return result.fetchall()

    def close(self):
        if self.engine:
            self.engine.dispose()
            print("Connection to MySQL database closed.")

db = MySQLDatabase(username="your_username",
                   password="your_password",
                   hostname="your_hostname",
                   port="your_port",
                   database_name="your_database_name")


#call this when we need to create a query to our database
db.connect()

query = "SELECT * FROM your_table_name"
data = db.execute_query(query)
print(data)

db.close()
