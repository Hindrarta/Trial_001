#!/usr/bin/env python
import pika, sys, os
from dotenv import load_dotenv
load_dotenv()

class rabbit:
    def __init__(self):
        self.rabbit_url = os.getenv("RABBITMQ_URL")
        self.rabbit_user = os.getenv("RABBITMQ_DEFAULT_USER")
        self.rabbit_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
        self.rabbit_port = eval(os.getenv("RABBITMQ_DEFAULT_PORT"))
        self.rabbit_exchange = os.getenv("RABBITMQ_DEFAULT_EXCHANGE")
        self.rabbit_credential = pika.PlainCredentials(self.rabbit_user, self.rabbit_pass)
        self.rabbit_parameters = pika.URLParameters("amqp://qblol:Pejaten13!@3.0.109.183:5672")
        self.connect()

    def connect(self):

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_url, 
                port=self.rabbit_port,
                credentials=self.rabbit_credential
                )
            )
        # self.connection = pika.BlockingConnection(self.rabbit_parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.rabbit_exchange)

        self.channel.basic_consume(queue=self.rabbit_exchange, on_message_callback=self.receiveCallback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def receiveCallback(self,ch, method, properties, body):
        print(f" [x] Received {body} - {method}")

if __name__ == '__main__':
    try:
        rabbitMQ = rabbit()
        print(f"rabbitmq url = {rabbitMQ.rabbit_url}")
    except Exception as e:
        print(f"Exception Occured, Reason : {e}")
    except KeyboardInterrupt:
        print("Keyboard Interrupt, System Exit . . . ")
        sys.exit(0)

