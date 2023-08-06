import select
import socket
from errno import EAGAIN
from typing import Callable

import attr
from logbook import Logger
from paho.mqtt.client import Client, MQTT_ERR_CONN_LOST, MQTT_ERR_UNKNOWN

from geli_python_common.amqp.amqp import MessageBusProtocol
from geli_python_common.amqp.message_bus_connector import Message, MessageBusConnector
from geli_python_common.util.constants import MAX_LOG_PAYLOAD_LENGTH

logger = Logger(__name__)


@attr.s
class MqttMessage(Message):
    retain = attr.ib(default=False)
    quality_of_service = attr.ib(default=0)


class PahoMessageBusConnector(MessageBusConnector):
    HEART_BEAT_SECONDS = 60 * 60
    LOOP_TIMEOUT = 1.0
    MAX_MESSAGES_PROCESSED_IN_ONE_LOOP = 10000
    MAX_ALLOWED_SUCCESSIVE_EMPTY_BUFFER = 3

    message_bus_protocol = MessageBusProtocol.MQTT

    def __init__(self, client_id, message_bus_host="127.0.0.1", message_bus_port=1883, loop_in_own_thread=True):
        """
        Create Paho MQTT message bus client.
        :param client_id: id name, auto-generated when empty
        :param message_bus_host: host address
        :param message_bus_port: host port
        :param loopInOwnThread: loop in own thread if True, otherwise ``loop`` needs to be called periodically to
        process messages
        """
        super().__init__(client_id=client_id,
                         message_bus_host=message_bus_host,
                         message_bus_port=message_bus_port,
                         loop_in_own_thread=loop_in_own_thread)
        self._client = PatchedClient(client_id, clean_session=True, userdata=id)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._handle_message
        self._client.on_disconnect = self._on_disconnect
        self._unexpected_disconnect = False

    def connect(self):
        self._client.connect(self._message_bus_host, self._message_bus_port, PahoMessageBusConnector.HEART_BEAT_SECONDS)

        # runs a thread in the background to call loop() automatically
        if self.loop_in_own_thread:
            self._client.loop_start()

    def disconnect(self):
        # disconnect client from broker
        self._client.disconnect()

        # stop thread
        if self.loop_in_own_thread:
            self._client.loop_stop()

        # close socket
        self._close_connection()

    def _register_callback(self, topic: str, callback: Callable):
        self._client.message_callback_add(topic, callback)
        self._client.subscribe(topic=topic)

    def send_message(self, message: MqttMessage):
        message_payload_json = message.payload.to_json()
        logger.trace("Sending {0} for resource {1}: {2}"
                     .format(type(message.payload).__name__, message.resource,
                             str(message_payload_json) if len(str(message_payload_json)) < MAX_LOG_PAYLOAD_LENGTH
                             else str(message_payload_json)[:MAX_LOG_PAYLOAD_LENGTH] + " ..."))
        self._client.publish(topic=message.resource,
                             payload=message_payload_json,
                             qos=message.quality_of_service,
                             retain=message.retain)

    def loop(self):
        """
        Run a loop cycle to process received messages. Needs to be regularly called if ``loop_in_own_thread``
        constructor parameter is False and should not be called at all if it's True.
        """
        if self.loop_in_own_thread:
            raise ValueError("Can't call loop if connector is running in its own thread")

        # A call to _client.loop() handles only a single message for some reason.
        # For processing messages at a reasonable rate it therefore needs to be called multiple times.
        empty_buffer_count = 0
        for _ in range(PahoMessageBusConnector.MAX_MESSAGES_PROCESSED_IN_ONE_LOOP):
            socket_buffer_empty = self._client.loop(timeout=0.001)[0]

            if socket_buffer_empty:
                empty_buffer_count += 1
            else:
                empty_buffer_count = 0

            if empty_buffer_count > PahoMessageBusConnector.MAX_ALLOWED_SUCCESSIVE_EMPTY_BUFFER:
                break
        else:
            logger.warn(
                f'Stopped churning through messages after handling {PahoMessageBusConnector.MAX_MESSAGES_PROCESSED_IN_ONE_LOOP} items. '
                f'This indicates a high message pressure or a large number of queued up elements.')

    def _handle_message(self, client, userdata, message):
        """
        Message handler for all topics which have no explicit handlers subscribed to.
        """
        logger.debug("Received unsubscribed message %s" % message.payload)

    def _on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from the server.
        """

        logger.info("%s connected with result code %s to broker %s:%d" % (self._client._client_id, rc,
                                                                          self._client.socket().getpeername()[0],
                                                                          self._client.socket().getpeername()[1]))
        if self._unexpected_disconnect:
            # Re-register subscriptions after disconnect
            self.subscribe(self._subscriptions)
            self._unexpected_disconnect = False

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warn("Unexpected message bus disconnection, code %s" % rc)
            if rc == 1:
                logger.warn("Possibly there is already another client connected with the same identifier")
            self._unexpected_disconnect = True

            logger.info("Trying to reconnect")
            self.connect()

    def _close_connection(self):
        # might not be necessary anymore when this issue gets addressed https://github.com/eclipse/paho.mqtt.python/issues/170
        if self._client._ssl:
            self._client._ssl.close()
            self._client._ssl = None
            self._client._sock = None
        elif self._client._sock:
            self._client._sock.close()
            self._client._sock = None
        if self._client._sockpairR:
            self._client._sockpairR.close()
        if self._client._sockpairW:
            self._client._sockpairW.close()


class PatchedClient(Client):
    """
    Paho MQTT client patched with method that returns if the socket buffers are empty.
    Based on paho-mqtt (1.3.1).
    """

    def loop(self, timeout=1.0, max_packets=1):
        """
        Patched base class method that adds a return value for when the socket buffers are empty, following the line
        ### ADDITION ###.
        """
        if timeout < 0.0:
            raise ValueError('Invalid timeout.')

        with self._current_out_packet_mutex:
            with self._out_packet_mutex:
                if self._current_out_packet is None and len(self._out_packet) > 0:
                    self._current_out_packet = self._out_packet.popleft()

                if self._current_out_packet:
                    wlist = [self._sock]
                else:
                    wlist = []

        # used to check if there are any bytes left in the (SSL) socket
        pending_bytes = 0
        if hasattr(self._sock, 'pending'):
            pending_bytes = self._sock.pending()

        # if bytes are pending do not wait in select
        if pending_bytes > 0:
            timeout = 0.0

        # sockpairR is used to break out of select() before the timeout, on a
        # call to publish() etc.
        rlist = [self._sock, self._sockpairR]
        try:
            socklist = select.select(rlist, wlist, [], timeout)
        except TypeError:
            # Socket isn't correct type, in likelihood connection is lost
            return MQTT_ERR_CONN_LOST
        except ValueError:
            # Can occur if we just reconnected but rlist/wlist contain a -1 for
            # some reason.
            return MQTT_ERR_CONN_LOST
        except KeyboardInterrupt:
            # Allow ^C to interrupt
            raise
        except:
            return MQTT_ERR_UNKNOWN

        if self._sock in socklist[0] or pending_bytes > 0:
            rc = self.loop_read(max_packets)
            if rc or self._sock is None:
                return rc

        if self._sockpairR in socklist[0]:
            # Stimulate output write even though we didn't ask for it, because
            # at that point the publish or other command wasn't present.
            socklist[1].insert(0, self._sock)
            # Clear sockpairR - only ever a single byte written.
            try:
                self._sockpairR.recv(1)
            except socket.error as err:
                if err.errno != EAGAIN:
                    raise

        if self._sock in socklist[1]:
            rc = self.loop_write(max_packets)
            if rc or self._sock is None:
                return rc

        ### ADDITION ###
        # socklist contains three empty lists if no data becomes available within timeout https://docs.python.org/2/library/select.html#select.select
        socket_buffer_empty = True
        for element in socklist:
            if element:
                socket_buffer_empty = False

        return (socket_buffer_empty, self.loop_misc())
