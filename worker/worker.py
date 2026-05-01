# worker/worker.py
import os
import pika
import json
import time
import sys

def main():
    rabbitmq_url = os.environ.get('RABBITMQ_URL')
    connection = None

    # Bucle para reintentar la conexión si RabbitMQ no está listo
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            print("Worker: Conectado a RabbitMQ.")
        except pika.exceptions.AMQPConnectionError:
            print("Worker: Esperando a RabbitMQ...")
            time.sleep(5)

    channel = connection.channel()
    
    # Declare Topic Exchange
    channel.exchange_declare(exchange='task_events', exchange_type='topic', durable=True)

    # Declare DLX and DLQ
    channel.exchange_declare(exchange='dlx', exchange_type='direct')
    channel.queue_declare(queue='tasks_failed', durable=True)
    channel.queue_bind(exchange='dlx', queue='tasks_failed', routing_key='task_created')

    # Declare main queue with DLX arguments
    args = {
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'task_created'
    }
    channel.queue_declare(queue='task_created', durable=True, arguments=args)
    channel.queue_bind(exchange='task_events', queue='task_created', routing_key='task.created')

    def callback(ch, method, properties, body):
        try:
            task_data = json.loads(body)
        except json.JSONDecodeError:
            print(" [!] Malformed JSON received. Rejecting.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        if 'title' not in task_data:
            print(" [!] Message missing 'title'. Rejecting.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        print(f" [x] Recibido y procesado nuevo task: ID={task_data.get('id')}, Título='{task_data.get('title')}'")
        # Aquí iría la lógica de procesamiento (enviar email, etc.)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='task_created', on_message_callback=callback)

    print(' [*] Esperando mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)