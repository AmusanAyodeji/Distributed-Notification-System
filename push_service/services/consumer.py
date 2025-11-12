import pika
import os
import json
import re
import ast
from dotenv import load_dotenv
from pusher import send_push

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def callback(ch, method, properties, body):
    # try:
        decoded_str = body.decode('utf-8')
        cleaned = re.sub(r"<NotificationType\.\w+: '(\w+)'>", r"'\1'", decoded_str)
        cleaned = re.sub(r"UUID\('([\w-]+)'\)", r"'\1'", cleaned)
        cleaned = re.sub(r"HttpUrl\('([^']+)'\)", r"'\1'", cleaned)
        notification = ast.literal_eval(cleaned)
        send_push(notification)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    # except Exception as e:
    #     print(f"PushService error: {e}")
    #     ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='push.queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.queue_bind(exchange='notifications.direct', routing_key='push.queue', queue="push.queue")
    channel.basic_consume(queue='push.queue', on_message_callback=callback)
    print("[PushService] Waiting for push messages...")
    channel.start_consuming()

start_consumer()