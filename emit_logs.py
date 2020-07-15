#!/usr/bin/env python
import pika
import sys
from param import parameters


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# routing_key value will be ignored through fanout exchange
# fanout exchange does not store any data but broadcasts all message to all queues binded to it instantly
# so if no queue is binded, the message sent to the exchange is gone.
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()