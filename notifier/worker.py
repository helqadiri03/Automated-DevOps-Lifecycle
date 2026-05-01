import os
import pika
import json
import time
import sys
import requests

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL')
    webhook_url = os.environ.get('WEBHOOK_URL')
    connection = None

    # Retry connection if RabbitMQ is not ready
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            print("Notifier: Connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError:
            print("Notifier: Waiting for RabbitMQ...")
            time.sleep(5)

    channel = connection.channel()
    
    # Declare Topic Exchange
    channel.exchange_declare(exchange='task_events', exchange_type='topic', durable=True)

    # Declare private queue for notifier
    channel.queue_declare(queue='notifier_task_completed', durable=True)
    channel.queue_bind(exchange='task_events', queue='notifier_task_completed', routing_key='task.completed')

    def callback(ch, method, properties, body):
        task_data = json.loads(body)
        print(f" [x] Received task completion: ID={task_data.get('id')}")
        
        if webhook_url:
            try:
                response = requests.post(webhook_url, json=task_data)
                print(f" [+] Notification sent to {webhook_url}. Status Code: {response.status_code}")
            except Exception as e:
                print(f" [-] Error sending notification: {e}")
        else:
            print(" [!] WEBHOOK_URL not set. Skipping notification.")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='notifier_task_completed', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
