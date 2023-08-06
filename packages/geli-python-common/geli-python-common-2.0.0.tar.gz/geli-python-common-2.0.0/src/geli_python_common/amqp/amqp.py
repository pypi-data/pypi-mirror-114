from datetime import timedelta, datetime
from time import sleep
from typing import Callable, Any, Dict

import attr
import pika
from aenum import auto
from attr import Factory
from logbook import Logger
from pika.exceptions import AMQPError

from geli_python_common.amqp.message_bus_connector import MessageBusConnector, Message
from geli_python_common.dto.dto import Dto
from geli_python_common.util.constants import MAX_LOG_PAYLOAD_LENGTH, CaseInsensitiveEnum, MAX_RETRY_COUNT

logger = Logger(__name__)


class MessageBusProtocol(CaseInsensitiveEnum):
    MQTT = auto()
    AMQP = auto()


@attr.s
class AmqpMessage(Message):
    eos_serial = attr.ib(default=None)
    exchange = attr.ib(default=None)
    properties = attr.ib(default=None, type=pika.spec.BasicProperties)
    routing_key = attr.ib(default=None)


class AmqpConfigArgument(CaseInsensitiveEnum):
    """
    AMQP configuration x-arguments
    """
    QUEUE_LENGTH = "x-max-length"
    # caution, there are different arguments for message and queue expiry
    MESSAGE_EXPIRY = "x-message-ttl"
    QUEUE_TTL = "x-expires"


class AmqpQueueParameter(CaseInsensitiveEnum):
    """
    Queue configuration parameters
    """
    AUTO_DELETE = "auto_delete"


@attr.s
class AmqpBlockingConnector(MessageBusConnector):
    """
    AMQP connector that uses blocking calls for simplicity. Have a look at the SelectConnection for implementing a
    more efficient async connector.
    """

    _username = attr.ib(default="geni")
    _password = attr.ib(default="1qazse4")

    _connection = attr.ib(default=None)
    _channel = attr.ib(default=None)
    _queues = attr.ib(default=Factory(dict))
    last_reconnect = attr.ib(init=False, type=datetime, default=None)
    message_bus_protocol = attr.ib(default=MessageBusProtocol.AMQP)
    _heart_beat = attr.ib(type=int, default=600)

    def connect(self):
        """
        Establish a connection with the broker and create a communication channel.
        :return:
        """
        logger.info(f'Connecting to {self._message_bus_host}:{self._message_bus_port} with client {self.client_id} '
                    f'as {self._username}')
        credentials = pika.PlainCredentials(self._username, self._password)
        parameters = pika.ConnectionParameters(host=self._message_bus_host,
                                               port=self._message_bus_port,
                                               credentials=credentials,
                                               heartbeat=self._heart_beat,
                                               blocked_connection_timeout=300
                                               )

        self._connection = pika.BlockingConnection(parameters=parameters)
        self._channel = self._connection.channel()

        self._channel.confirm_delivery()

    def loop(self, timeout=timedelta(seconds=10)):
        """
        This method fetches all messages from the queues the connector is subscribed to.
        :param timeout: duration in <timedelta> after which queue processing is aborted, CAUTION: depends on underlying IO loop and has been unreliable
        :return:
        """
        # Check that consumers exist on this channel
        if self._channel._consumer_infos:
            # TODO timeout isn't respected / doesn't cause preemption (at least in tested sub-second range)
            self._channel.connection.process_data_events(timeout.total_seconds())

    def loop_forever(self):
        """
        Note: This method blocks infinitely

        This method fetches all messages from the queues the connector is subscribed to. The start_consuming is a blocking call and does
        not return after fetching a message. It blocks for ever, until stop_consuming() is called.
        :return:
        """

        self._channel.start_consuming()

    def send_message(self, message: AmqpMessage, retry_forever: bool = True) -> bool:
        """
        Send a message to the broker.
        :param: message: message which contains payload and exchange
        :param: retry_forever: retry forever if retry_forever is true, else retry for 3 times
        :return: True/False
        """
        # check exchange type is str or enum
        if isinstance(message.exchange, str):
            exchange = message.exchange
        else:
            exchange = message.exchange.value

        # check payload is str or dto
        if isinstance(message.payload, str):
            message_payload_json = message.payload
        else:
            message_payload_json = message.payload.to_json()

        message_sent = False
        retry_count = 1
        while retry_forever or retry_count >= 0:
            retry_count = retry_count - 1
            try:
                logger.trace("Sending {0} to exchange {1} with routing key {2}: {3}"
                             .format(type(message.payload).__name__, message.exchange, message.routing_key,
                                     str(message_payload_json) if len(
                                         str(message_payload_json)) < MAX_LOG_PAYLOAD_LENGTH
                                     else str(message_payload_json)[:MAX_LOG_PAYLOAD_LENGTH] + " ..."))

                self._channel.basic_publish(exchange=exchange,
                                            routing_key=message.routing_key,
                                            body=message_payload_json,
                                            properties=message.properties)
                message_sent = True
                break
            except AMQPError as ex:
                sub_string_message_payload_json = ""
                if len(str(message_payload_json)) > 50:
                    sub_string_message_payload_json = message_payload_json[0:50]

                logger.error(f'Failed to publish the message {sub_string_message_payload_json} due to {ex}. '
                             f'Retrying to connect and re-publishing message')
                self.reconnect(retry_forever=retry_forever)
            except pika.exceptions.UnroutableError as ure:
                logger.error(f"Message could not be delivered {ure}")
                self.reconnect(retry_forever=retry_forever)
            except Exception as e:
                logger.error(f'Failed to publish the message due to {e}')
                break

            # Retry after 2 seconds
            sleep(2)

        return message_sent

    def _register_callback(self, queue: str, callback: Callable):
        self.register_queue_consumer(queue=queue, consumer=callback)

    def register_queue(self,
                       queue: str,
                       routing_key: str,
                       exchange: str,
                       durable: bool = False,
                       queue_arguments: Dict[AmqpConfigArgument, Any] = None,
                       queue_parameters: Dict[AmqpQueueParameter, Any] = None):
        """
         Register queue to the exchange.
        :param queue: queue name
        :param routing_key: routing key
        :param exchange: exchange name
        :param durable: Survive queue after restart broker if it is true else delete from broker
        :param queue_arguments: queue arguments
        :param queue_parameters: queue parameters
        """
        if not queue_arguments:
            queue_arguments = {}
        if not queue_parameters:
            queue_parameters = {}

        self._channel.queue_declare(queue=queue,
                                    durable=durable,
                                    arguments={enum.value: value for enum, value in queue_arguments.items()},
                                    **{enum.value: value for enum, value in queue_parameters.items()})

        self._channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

        # add empty queue - consumer mapping to keep track of registered queues
        self._queues[queue] = None
        logger.debug(f'Bound queue {queue} to exchange {exchange} with routing key {routing_key}')

    def register_queue_consumer(self, queue, consumer, persist_queue=True):
        """
        Register callback for arriving messages on that queue.
        :param queue: queue name
        :param consumer: callback function
        :param persist_queue: flag if the queue should be persisted in the connector and survive disconnect
        :return:
        """
        if persist_queue:
            self._queues[queue] = consumer

        self._channel.basic_consume(queue=queue, on_message_callback=consumer)

    def disconnect(self):
        """
        Stop consuming messages from the broker and close the connection
        :return:
        """
        if not self._channel.is_closed:
            self._channel.stop_consuming()
            self._connection.close()
            logger.info(f'Disconnected client {self.client_id}')

    def reconnect(self, retry_forever: bool = True) -> bool:
        """
        AMQP re-connect helper function
        :param: retry forever if retry_forever is true, else retry for 3 times
        :return: bool - True/False
        """
        logger.info(f'Reconnecting to AMQP')
        retry_count = 0
        reconnected = False
        while retry_forever or retry_count < 3:

            # Disconnect the AMQP connection
            try:
                self.disconnect()
            except Exception as e:
                logger.error(f'Error in Disconnecting: {e}')

            sleep(1)

            # Re-establish the AMQP connection
            try:
                self.connect()
                reconnected = True
                break
            except Exception as e:
                logger.error(f'Error in Reconnecting: {e}')

            retry_count += 1

            # Retry after 2 seconds
            sleep(2)

        return reconnected

    def check_if_exchange_exists(self, exchange: str, retry_forever: bool = False) -> bool:
        """
        Checks exchange is available or not.
        :param exchange: exchange name
        :param retry_forever: retry until the exchange is created.
        :return: True if exchange already exists else return False
        """
        exchange_exist = False
        while True:
            try:
                self._channel.exchange_declare(exchange=exchange, passive=True)
                exchange_exist = True
                break
            except AMQPError as e:
                logger.error(f'{exchange} exchange does not exist {e}')
                # reconnect is required when channel is closed
                self.reconnect(retry_forever=retry_forever)

            if not retry_forever:
                break

            # wait for 10 seconds before retry
            sleep(10)

        return exchange_exist
