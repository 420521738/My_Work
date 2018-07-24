import pika,time
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='q8')



def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    #connection.sleep( body.count('.') )
    print " [x] Done"

channel.basic_consume(callback,queue='q8')
connection.close()
    
    

