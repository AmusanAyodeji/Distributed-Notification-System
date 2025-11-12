from schema.templates import TemplateCreate, Template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

def init_db_connection():
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        cursor = connection.cursor()
        return connection, cursor   
    except Exception as e:
        print(f"Failed to connect: {e}")

def create_template(template_data: dict):
    template = TemplateCreate(**template_data)
    conn, cur = init_db_connection()
    cur.execute("INSERT INTO templates (code, subject, body, language_code, version) VALUES (%s, %s, %s, %s, %s)",(template.code, template.subject, template.body, template.language_code, template.version))
    conn.commit()
    cur.close()
    conn.close()
    return template

def get_template_by_code(code: str, language_code="en", version=None):
    conn, cur = init_db_connection()
    query = "SELECT * FROM templates WHERE code=%s AND language_code=%s"
    vars = (code, language_code)
    if version:
        query += " AND version=%s" 
        vars = (code, language_code, version)

    cur.execute(query,vars)
    template = cur.fetchone()
    cur.close()
    conn.close()
    if not template:
        return None
    return Template(
        code=template[1],
        subject=template[2],
        body=template[3],
        language_code=template[4],
        version=template[5]
    )

def fill_template(template_body: str, variables: dict):
    try:
        return template_body.format(**variables)
    except Exception as e:
        return template_body

