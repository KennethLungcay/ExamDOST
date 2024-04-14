from sqlalchemy import create_engine, text, insert, MetaData,Column,String
from sqlalchemy.schema import Table


class MySQLDatabase:
    def __init__(self, username, password, hostname, port, database_name):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database_name = database_name
        self.metadata = MetaData() 
        self.engine = None

    def connect(self):
        if not self.engine:
            connection_string = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_name}"
            self.engine = create_engine(connection_string)
            

    def execute_query(self, query):
        if not self.engine:
            self.connect()
        with self.engine.connect() as connection:
            stmt = text(query)  # Convert query string to SQLAlchemy text object
            result = connection.execute(stmt)  # Execute the statement object
            return result.fetchall()
    
    def execute_insert(self, table_name, **kwargs):
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as connection:
                metadata = MetaData()  # Initialize the MetaData object without the 'bind' argument
                table = Table(table_name, metadata, autoload_with=self.engine)
                metadata.reflect(bind=self.engine)
                stmt = table.insert().values(**kwargs)
                connection.execute(stmt)
                print(f"Inserted data into {table_name}.")
                # Commit the transaction
                connection.commit()
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")

    def execute_update(self, table_name, condition_column, condition_value, update_values):
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as connection:
                metadata = MetaData()  # Initialize the MetaData object without the 'bind' argument
                table = Table(table_name, metadata, autoload_with=self.engine)
                metadata.reflect(bind=self.engine)

                # Construct the update statement
                stmt = (
                    table.update()
                    .where(getattr(table.c, condition_column) == condition_value)
                    .values(**update_values)
                )

                # Execute the update statement
                connection.execute(stmt)
                print(f"Updated data in {table_name}.")
                # Commit the transaction
                connection.commit()
        except Exception as e:
            print(f"Error updating data in {table_name}: {e}")


    def delete_data(self, id_to_delete):
        if not self.engine:
            self.connect()
        with self.engine.connect() as connection:
            stmt = text(f"DELETE FROM states WHERE id='{id_to_delete}'")  # Convert query string to SQLAlchemy text object
            result = connection.execute(stmt)  # Execute the statement object
            connection.commit()  # Commit the transaction
            return result.rowcount  # Returns the number of rows affected by the query




    def close(self):
        if self.engine:
            self.engine.dispose()
            print("Connection to MySQL database closed.")

db = MySQLDatabase(username="kenneth",
                    password="password",
                    hostname="localhost",
                    port="3306", 
                    database_name="examdostDB")





                