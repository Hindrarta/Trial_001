#!/usr/bin/env python
import pika, sys, os
import datetime
import time
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


    def PubMsg(self):

        date = str(datetime.datetime.now())
        self.channel.basic_publish(exchange='', routing_key=self.rabbit_exchange, body=date)
        print(f"Msg = {type(date)} {date}")

if __name__ == '__main__':
    try:
        rabbitMQ = rabbit()
        print(f"Connected to rabbitmq url = {rabbitMQ.rabbit_url}")
    except Exception as e:
        print(f"Cannot Connect RabbitMQ, reason {e}:")
        sys.exit(0)
    
    while True:
        try:
            rabbitMQ.PubMsg()
        except Exception as e:
            print(f"Exception Occured, Reason : {e}")
        except KeyboardInterrupt:
            print("Keyboard Interrupt, System Exit . . . ")
            rabbitMQ.connection.close()
            sys.exit(0)
        time.sleep(5)

