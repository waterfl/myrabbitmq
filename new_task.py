#!/usr/bin/env python
import pika
import sys
from param import parameters


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# queue should be durable
# notice: !queue is only a container and message will be lost after rabbit-server service restart even if queue is durable
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    # message should be persistent that will be written into disk so message will not be lost after rabbit-server service restart normally
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()