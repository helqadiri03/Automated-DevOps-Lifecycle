import os
import pika
import time
import sys
import json

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL')
    connection = None

    # Retry connection
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            print("ErrorHandler: Connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError:
            print("ErrorHandler: Waiting for RabbitMQ...")
            time.sleep(5)

    channel = connection.channel()
    
    # Declare DLX and DLQ (idempotent)
    channel.exchange_declare(exchange='dlx', exchange_type='direct')
    channel.queue_declare(queue='tasks_failed', durable=True)
    channel.queue_bind(exchange='dlx', queue='tasks_failed', routing_key='task_created')

    def callback(ch, method, properties, body):
        print(f" [x] FAILED TASK RECEIVED: {body}")
        # Here we could log to a file or database
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='tasks_failed', on_message_callback=callback)

    print(' [*] Waiting for failed messages. To exit press CTRL+C')
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
