from fastapi import FastAPI
import os
import mysql.connector
from mysql.connector import Error

app = FastAPI()

__version__ = "1.0.0"


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


def db_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )
        if connection.is_connected():
            return connection, "Successful connection"
    except Error as e:
        return None, f"Unsuccessful connection: {str(e)}"


def test_db_connection() -> str:
    _, message = db_connection()
    return message


@app.get("/healthcheck")
def healthcheck():
    return {
        "name": "devops_project API",
        "version": __version__,
        "status": {"application": "running", "database": test_db_connection()},
    }


@app.get("/education-name-logo")
def education_name_logo():
    connection, message = db_connection()
    if not connection:
        return {"error": message}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, logo FROM education")
        results = cursor.fetchall()
        print(type(results))
        return {"education": results}

    except Error as e:
        return {"error": f"Query failed: {str(e)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


@app.get("/domain_skills")
def domain_skills():
    connection, message = db_connection()
    if not connection:
        return {"error": message}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM domain_skills")
        results = cursor.fetchall()
        return {"domain_skills": results}

    except Error as e:
        return {"error": f"Query failed: {str(e)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()
