#!/usr/bin/env python
import pika
from param import parameters


connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,    # messsage through default direct exchange with routing_key 
                                                        # will be delivered to the queue with the name as props.reply_to
                                                            # which is the task result queue defined by the rpc client
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                                                    # task id
                                                        # which tells which task the result computed belongs to.
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()