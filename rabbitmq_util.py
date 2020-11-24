import pika

from common import const


def get_connection():
    credentials = pika.PlainCredentials(const.RABBITMQ_USERNAME, const.RABBITMQ_PASSWORD)  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=const.RABBITMQ_HOST, port=const.RABBITMQ_PORT, virtual_host=const.VIRTUAL_HOST,
                                  credentials=credentials))
    return connection


def send_message(queue, routing_key, exchange, message, exchange_type='direct'):
    connection = get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message
                          )
    connection.close()


def receive_message(queue, routing_key, exchange, callback, exchange_type='direct'):
    connection = get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    channel.basic_consume(queue, callback)
    channel.start_consuming()


def print_mq(channel, method, properties, bodyx):
    print("队列名(订阅的主题名）为：%r  得到的数据为:%r  " % (method.routing_key, bodyx))
    send_message("test_return_queue", "test.return", "direct", "successful get message!")
    channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    receive_message("test", "test", "direct", print_mq)
