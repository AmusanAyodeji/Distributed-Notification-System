import os
import httpx
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException
import psycopg2
import json
import ast

load_dotenv()

VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_EMAIL = os.getenv("VAPID_EMAIL")
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

def send_push(data: dict):
    response = httpx.post(f"http://127.0.0.1:8001/api/v1/templates/fill/?code={data.get('template_code')}&language_code={data.get("language_code", "en")}", json=data.get("variables"))
    template_response = response.json()
    template = template_response.get("data", {}).get("body", "")
    conn, cur = init_db_connection()
    cur.execute("SELECT push_token FROM users WHERE id = %s",(str(data.get("user_id")),))
    user = cur.fetchone()
    if not user or not user[0]:
        print(f"No push token found for user ID {data.get('user_id')}")
        return
    cur.close()
    conn.close()
    try:
        webpush(
            subscription_info=ast.literal_eval(user[0]),
            data=template,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_EMAIL}
        )
    except WebPushException as e:
        print(f"An error occured:{e}")
