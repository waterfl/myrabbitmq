#!/usr/bin/env python
import pika
import time
from param import parameters


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # message handled fully ensured
    ch.basic_ack(delivery_tag=method.delivery_tag)


# we should be fair and have a look at the workers' load
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

# what's more we can also set message time-to-live so that old message will be dropped automatically while the message is too heavy for the workers
