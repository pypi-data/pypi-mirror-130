import json
import pika, sys, os
from ..config import AMQP_CONFIG


from ..modules.rest.business import pika_create_change_event

def main():

    cred = pika.PlainCredentials(AMQP_CONFIG['AMQP_USER'], AMQP_CONFIG['AMQP_PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=AMQP_CONFIG['AMQP_HOST'], credentials=cred, virtual_host=AMQP_CONFIG['AMQP_VIRTUAL_HOST']))
    channel = connection.channel()

    channel.queue_declare(queue=AMQP_CONFIG['AMQP_QUEUE'], durable=True)
    severities = sys.argv[1:]
    for severity in severities:
        channel.queue_bind(
            exchange=AMQP_CONFIG['AMQP_EXCHANGE'], queue=AMQP_CONFIG['AMQP_QUEUE'], routing_key=AMQP_CONFIG['AMQP_ROUTING_KEY'])

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        data = body.decode('utf-8')
        data = json.loads(data)
        pika_create_change_event(data=data)

    channel.basic_consume(queue=AMQP_CONFIG['AMQP_QUEUE'], on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)