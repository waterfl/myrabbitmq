#!/usr/bin/env python
import pika
from param import parameters


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# queue declared        
# notice:   queue will be lost or deleted after restarting the rabbitmq-server
channel.queue_declare(queue='hello')

# message published via the default exchange with "direct" type
# so here message with routing_key 'hello' will be sent to queue 'hello'
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()