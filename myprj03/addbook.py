import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='mj',
            user='mj',
            password='0000'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        return None

def fetch_table_names(conn):
    if conn is None:
        print("Database connection is not established.")
        return []  # 데이터베이스 연결이 실패하면 빈 리스트 반환
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except Error as e:
        print(e)
        return []


def fetch_table_data(conn, table_name):
    if conn is None:
        print("Database connection is not established.")
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []

def show_table_contents(event):
    selected_table = table_listbox.get(table_listbox.curselection())
    table_data = fetch_table_data(conn, selected_table)
    if table_data:
        tree.delete(*tree.get_children())
        for row in table_data:
            tree.insert("", tk.END, values=row)

root = tk.Tk()
root.title("MySQL Table Viewer")

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

table_listbox = tk.Listbox(table_frame)
table_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
table_listbox.config(yscrollcommand=scrollbar.set)

tree = ttk.Treeview(root)
tree.pack(fill=tk.BOTH, expand=True)

table_listbox.bind("<<ListboxSelect>>", show_table_contents)

# MySQL 데이터베이스 연결
conn = connect_to_database()

# 테이블 이름 가져오기
table_names = fetch_table_names(conn)
for table_name in table_names:
    table_listbox.insert(tk.END, table_name)

root.mainloop()
