import streamlit as st
import mysql.connector
past_operations=[["Task Name", "Task Query", "Status"]]
connections = [
    {"name": "connection", "host": "localhost", "port": 3009, "user": "root", "password": "some_pass"},
    {"name": "connection1", "host": "localhost", "port": 3014, "user": "root", "password": "some_pass"},
    {"name": "connection2", "host": "localhost", "port": 3015, "user": "root", "password": "some_pass"},
    {"name": "connection3", "host": "localhost", "port": 3016, "user": "root", "password": "some_pass"},
    {"name": "connection4", "host": "localhost", "port": 3017, "user": "root", "password": "some_pass"},
    {"name": "connection5", "host": "localhost", "port": 3018, "user": "root", "password": "some_pass"}
]

def list_databases(connection_name):
    try:
        for conn_info in connections:
            if conn_info["name"] == connection_name:
                connection = mysql.connector.connect(
                    host=conn_info["host"],
                    port=conn_info["port"],
                    user=conn_info["user"],
                    password=conn_info["password"]
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("SHOW DATABASES")
                    databases = [db[0] for db in cursor.fetchall()]
                    cursor.close()
                    connection.close()
                    return databases

    except mysql.connector.Error as error:
        st.error(f"Error while connecting to MySQL: {error}")
        return []


def execute_crud_operation(operation, connection_name, *args):
    try:
        for conn_info in connections:
            connection = mysql.connector.connect(
                host=conn_info["host"],
                port=conn_info["port"],
                user=conn_info["user"],
                password=conn_info["password"]
            )

            if connection.is_connected():
                cursor = connection.cursor()

                if operation == "use_database":
                    database_name = args[0]
                    cursor.execute("SHOW DATABASES")
                    existing_databases = [db[0] for db in cursor.fetchall()]
                    if database_name not in existing_databases:
                        cursor.execute(f"CREATE DATABASE {database_name}")
                    cursor.execute(f"USE {database_name}")
                if operation == "create_database":
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {args[0]}")
                    
                connection.commit()
                cursor.close()
                connection.close()  

    except mysql.connector.Error as error:
        st.error(f"Error while connecting to MySQL: {error}")

def crud_operation(query, *args):

    name=args[2]
    database_name = args[1]
    try:
        for conn_info in connections:
            connection = mysql.connector.connect(
                host=conn_info["host"],
                port=conn_info["port"],
                user=conn_info["user"],
                password=conn_info["password"]
            )

            if connection.is_connected():
                cursor = connection.cursor()
                
                cursor.execute(f"USE {database_name}")
                cursor.execute(query);                    
                connection.commit()
                cursor.close()
                connection.close()  
        past_operations.append([name,query,"Success"])
        print(past_operations)


    except mysql.connector.Error as error:
        past_operations.append([name,query,"Failure"])
        print(past_operations)
        st.error(f"Error while connecting to MySQL: {error}")


def main():
    st.title("Task Manager")
    menu = ["Add Operation", "View Past Operations"]
    choice = st.sidebar.selectbox("Menu", menu)

    connection_name = "connection" 

    if choice == "Add Operation":
        databases = list_databases(connection_name)
        selected_db = st.selectbox("Select Database", databases + ["Create New Database"])
        if selected_db == "Create New Database":
            new_db_name = st.text_input("Enter New Database Name")
            if st.button("Create"):
                execute_crud_operation("create_database", connection_name, new_db_name)
        else:
            execute_crud_operation("use_database", connection_name, selected_db)
        task_name = st.text_input("Name of the Task")
        task_query = st.text_input("Enter SQL command ")
        if st.button("Add Task"):
            crud_operation(task_query,connection_name, selected_db,task_name)
            pass
    elif choice == "View Past Operations":
        print(past_operations)
        st.title("Past Operations")
        st.table(past_operations)
        pass

if __name__ == "__main__":
    main()
