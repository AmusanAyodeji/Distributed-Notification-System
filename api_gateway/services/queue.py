import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def send_to_queue(queue_name:str, message:dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='notifications.direct',
        exchange_type='direct'
    )
    channel.basic_publish(
        exchange='notifications.direct',
        routing_key=queue_name,
        body=str(message)
    )


