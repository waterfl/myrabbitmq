#!/usr/bin/env python
import pika
import uuid
from param import parameters


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue           # task result queue

        self.channel.basic_consume(                 # check task result process 
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body): # check task result queue and get task result via task id
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())                    # task id
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,               # task result to task queue
                correlation_id=self.corr_id,                # task id in task queue
            ),
            body=str(n))
                                                    # task published
        while self.response is None:
            self.connection.process_data_events()           # check task result - non blocking consuming
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)