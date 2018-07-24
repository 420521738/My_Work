import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='q1')



def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback,queue='q1',no_ack=True)
    
    
    