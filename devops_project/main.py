from fastapi import FastAPI
import os
import mysql.connector
from mysql.connector import Error

app = FastAPI()

__version__ = "1.0.0"


# Lire les variables d'environnement
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # Host = nom du service docker mysql
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"



def test_db_connection() -> str:
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if connection.is_connected():
            return "Successful connexion"
    except Error as e:
        return "Unsuccessful connection"
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()


@app.get("/healthcheck")
def root():
    return {
        "name": "devops_project API", 
        "version": __version__, 
        "status": {
            "application": "running",
            "database": test_db_connection()
        }
    }
