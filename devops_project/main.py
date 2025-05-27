from fastapi import FastAPI

app = FastAPI()

__version__ = "1.0.0"




# Lire les variables d'environnement
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # Host = nom du service docker mysql
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


@app.get("/healthcheck")
def root():
    return {"name": "devops_project API", "version": __version__, "status": "running"}