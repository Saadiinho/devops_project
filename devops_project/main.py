import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__version__ = "1.0.0"


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# DB_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}" Ne sert à rien ?


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


class EducationNameLogo(BaseModel):
    name: str
    logo: str


@app.get("/education-name-logo", response_model=List[EducationNameLogo])
def education_name_logo():
    connection, message = db_connection()
    if not connection:
        return {"error": message}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, logo FROM education")
        results = cursor.fetchall()
        return results

    except Error as e:
        return {"error": f"Query failed: {str(e)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


class Skill(BaseModel):
    domain: str
    skill: str
    icone: str
    course: bool


@app.get("/skills", response_model=List[Skill])
def skills():
    connection, message = db_connection()
    if not connection:
        return {"error": message}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
                SELECT ds.name AS domain, s.name AS skill, s.icone, s.course
                FROM domain_skills_links dsl
                JOIN skills s ON dsl.skill_id = s.skills_id
                JOIN domain_skills ds ON dsl.domain_id = ds.id
            """
        )
        results = cursor.fetchall()
        return results
    except Error as e:
        return {"error": f"Query failed: {str(e)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


class Project(BaseModel):
    project_id: int
    name: str
    description: str
    icone: str
    link: str
    domain: str
    long_description: str
    features: str
    isWebsite: bool
    demonstrate: bool


@app.get("/projects", response_model=List[Project])
def projects():
    connection, message = db_connection()
    if not connection:
        return {"error": message}
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM project ORDER BY domain"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        connection.close()


@app.get("/projects/{domain}", response_model=List[Project])
def projects_by_domain(domain: str):
    connection, message = db_connection()
    if not connection:
        return {"error": message}
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM project WHERE domain = %s"
        cursor.execute(query, (domain,))
        results = cursor.fetchall()
        return results
    except Error as e:
        return {"error": f"Query failed: {str(e)}"}
    finally:
        if connection.is_connected():
            connection.close()


@app.get("/project/{project_id}", response_model=Project)
def get_project(project_id: int):
    connection, message = db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=message)

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM project WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()

        if project:
            return project
        raise HTTPException(status_code=404, detail="Projet introuvable")

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


class Education(BaseModel):
    education_id: int
    name: str
    title: str
    description: str
    logo: str
    link: str
    recommandation: str | None
    date: str
    education: bool


@app.get("/educations", response_model=List[Education])
def get_educations(education: Optional[int] = Query(None, ge=0, le=1)):
    """
    Retourne les parcours scolaire (education=1) ou professionnels (education=0).
    Si aucun filtre n'est passé, retourne tout.
    """
    connection, message = db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail=message)

    try:
        cursor = connection.cursor(dictionary=True)

        if education is not None:
            cursor.execute(
                "SELECT * FROM education WHERE education = %s ORDER BY education_id DESC",
                (education,),
            )
        else:
            cursor.execute("SELECT * FROM education ORDER BY education_id DESC")

        results = cursor.fetchall()
        return results

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


class DomainSkill(BaseModel):
    id: int
    name: str


@app.get("/domain-skills", response_model=List[DomainSkill])
def domain_skills():
    connection, message = db_connection()
    if not connection:
        return {"error": message}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM domain_skills")
        results = cursor.fetchall()
        return results

    except Error as e:
        return {"error": f"Query failed: {str(e)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()


SENDER_EMAIL = os.getenv("SMTP_USER")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "toi@exemple.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


class Mail(BaseModel):
    first_name: str
    last_name: str
    email: str
    compagny: str | None
    message: str


@app.post("/send-mail")
def send_mail(mail: Mail):
    try:
        # Création du message
        msg = MIMEMultipart()
        msg["From"] = mail.email
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"Message de contact de {mail.first_name} {mail.last_name}"

        body = f"""
        Nom : {mail.first_name} {mail.last_name}
        Email : {mail.email}
        Entreprise : {mail.company or 'Aucune'}
        
        Message :
        {mail.message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(mail.email, RECEIVER_EMAIL, msg.as_string())

        return {"message": "Email envoyé avec succès"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Échec de l'envoi de l'email : {str(e)}"
        )
