import pika
import os
"""
    CREATE USER:
        rabbitmqctl add_user Username Password
    SET USER TAGS:
        rabbitmqctl set_user_tags User Tag               # For web login
    SET PERMISSIONS:
        rabbitmqctl set_permissions -p VHostPath User ConfP WriteP ReadP    # For pika login
"""


HOST = os.environ['rbt_host'].strip()
USER = os.environ['rbt_user'].strip()
PASSWORD = os.environ['rbt_pass'].strip()

credentials = pika.PlainCredentials(USER, PASSWORD)
parameters = pika.ConnectionParameters(host=HOST, credentials=credentials)