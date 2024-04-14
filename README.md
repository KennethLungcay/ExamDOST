Activate Virtual Environment:

    Open your command prompt or terminal.
    Navigate to the root directory of your project using the cd command. For example:
    $ cd path/to/your/project

    Next, go to the PracticalExamDOST_env/scripts directory:
    $ cd PracticalExamDOST_env/scripts

    Activate the virtual environment:
    $ activate

    Now, return to the root folder:
    $ cd ..

Install Dependencies:

    Go to the PracticalExamDOST directory:
    $ cd PracticalExamDOST

    Install all the required dependencies from the requirements.txt file:
    $ pip install -r requirements.txt

Run the Apache Server for the Database:

    Ensure that you have Apache installed and running.
    Import the database schema (SQL file) into your local MySQL server.
    Configure the Database Engine:
    Locate the db_connector.py file in the PracticalExamDOST folder.
    Edit the following parameters in the file:
    engine: Set it to your database engine (e.g., MySQL, PostgreSQL).
    user: Your database username.
    password: Your database password.
    port: The port number for your database server.
    host: The hostname or IP address of your database server.
    db_name: The name of your database.

Run the Main Application:

    Execute the following command in the terminal:
    $ cd PracticalExamDOST
    $ streamlit run main.py
