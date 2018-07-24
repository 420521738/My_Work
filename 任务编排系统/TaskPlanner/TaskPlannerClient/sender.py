import pika,sys

msg = ' '.join(sys.argv[1:] or "Hello World")
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
#channel.basic_qos(prefetch_count=1)
channel.queue_declare(queue='q8')
channel.basic_publish(exchange='',
                      routing_key='q8',
                      body=msg,
                      properties = pika.BasicProperties(
                        delivery_mode=2,
                       ))
print "[X] send '%r'" % (msg,)
connection.close()
