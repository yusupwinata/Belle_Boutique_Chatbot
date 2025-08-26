import os
import sqlite3
import pandas as pd
from pathlib import Path

# Paths
ABSOLUTE_PATH = Path(__file__).resolve().parent.parent.parent
sql_path = os.path.join(ABSOLUTE_PATH, "data", "sql")

# Files
db = os.path.join(sql_path, "butik_database.db") # butik_database_testing.db | butik_database.db

class SQL:
    """Load and manipulate the database"""
    connection = None
    cursor = None

    chat_history_limit = 3

    def __init__(self):
        if not self.connection:
            self.__class__.create_connection()
    
    def get_order_status(self, nomor_resi: str) -> dict:
        try:
            query = "SELECT * FROM orders WHERE no_resi = ?"
            df = pd.read_sql_query(query, self.connection, params=(nomor_resi,))

            if df.empty:
                return {"error": "nomor resi tidak ditemukan dalam database"}

            result = df.to_dict(orient='index')
            return result[0]
        except Exception as e:
            return {f"Error while getting order status from the database: {str(e)}"}
    
    def get_chat_history(self) -> pd.DataFrame:
        query = "SELECT * FROM chat_history ORDER BY created_at DESC LIMIT ?"
        df = pd.read_sql_query(query, self.connection, params=(self.chat_history_limit,))
        return df[["user_message", "assistant_message"]]
    
    def save_chat_history(self, user_message: str, assistant_message: str) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO chat_history (user_message, assistant_message) VALUES (?, ?)",
                (user_message, assistant_message)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error while saving chat history: {str(e)}")
            print(f"user_message: {user_message}")
            print(f"assistant_message: {assistant_message}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    @classmethod
    def create_connection(cls) -> None:
        try:
            cls.connection = sqlite3.connect(db)
            cls.cursor = cls.connection.cursor()
        except Exception as e:
            raise Exception(f"Error while connecting to the database: {str(e)}")