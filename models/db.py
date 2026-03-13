import mysql.connector
from mysql.connector import Error
import streamlit as st

class DatabaseConnection:
    def __init__(self, host=None, user=None, password=None, database=None):
        # Load from Streamlit secrets if available, else use defaults
        try:
            secrets = st.secrets["mysql"]
            self.host = host or secrets["host"]
            self.user = user or secrets["user"]
            self.password = password or secrets["password"]
            self.database = database or secrets["database"]
        except (KeyError, FileNotFoundError):
            # Fallback for local development
            self.host = host or 'localhost'
            self.user = user or 'root'
            self.password = password or ''
            self.database = database or 'IT20FinalProj'
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            st.error(f"Error connecting to MySQL: {e}")
            return None

    def create_database(self):
        """Create database if not exists"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            conn.close()
        except Error as e:
            st.error(f"Error creating database: {e}")

    def create_table(self):
        """Create predictions table if not exists"""
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                create_table_query = """
                CREATE TABLE IF NOT EXISTS predictions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    credit_score INT,
                    age INT,
                    tenure INT,
                    balance FLOAT,
                    num_products INT,
                    has_card INT,
                    active_member INT,
                    salary FLOAT,
                    geography_germany INT,
                    geography_spain INT,
                    gender_male INT,
                    prediction VARCHAR(20),
                    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                conn.commit()
                cursor.close()
                conn.close()
        except Error as e:
            st.error(f"Error creating table: {e}")

    def insert_prediction(self, data):
        """Insert prediction record into database"""
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                insert_query = """
                INSERT INTO predictions 
                (credit_score, age, tenure, balance, num_products, has_card, 
                 active_member, salary, geography_germany, geography_spain, 
                 gender_male, prediction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, data)
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Error as e:
            st.error(f"Error inserting prediction: {e}")
            return False

    def get_prediction_history(self):
        """Retrieve all predictions from database"""
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM predictions ORDER BY prediction_date DESC")
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
        except Error as e:
            st.error(f"Error retrieving predictions: {e}")
            return []

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()