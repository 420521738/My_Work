import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='q1')
channel.basic_publish(exchange='',
                      routing_key='q1',
                      body='fuck it...')
print "[X] send 'fuck.'"