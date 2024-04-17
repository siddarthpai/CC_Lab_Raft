# app.py
import streamlit as st
import sqlite3
from datetime import datetime

 
def create_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

 
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            due_date TEXT
        )
    ''')
    conn.commit()

 
def insert_task(conn, name, description, due_date):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (name, description, due_date) VALUES (?, ?, ?)
    ''', (name, description, due_date))
    conn.commit()
  
def get_tasks(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()

 
def main():
 
    conn = create_connection()
    create_table(conn)

    
    st.title('Task Management App')

    
    st.subheader('Add New Task')
    task_name = st.text_input('Task Name')
    task_description = st.text_area('Task Description')
    task_due_date = st.date_input('Due Date')
    if st.button('Add Task'):
        insert_task(conn, task_name, task_description, task_due_date)
        st.success('Task added successfully!')

    # Display the list of tasks
    st.subheader('Tasks')
    tasks = get_tasks(conn)
    for task in tasks:
        st.write(f"**{task[1]}**")
        st.write(f"Description: {task[2]}")
        st.write(f"Due Date: {task[3]}")
        st.write("---")

if __name__ == "__main__":
    main()
