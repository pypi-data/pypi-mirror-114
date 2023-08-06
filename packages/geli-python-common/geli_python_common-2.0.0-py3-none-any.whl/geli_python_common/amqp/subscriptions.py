import attr
from abc import ABC
from functools import partial
from logbook import Logger
from typing import Callable, Union, Type

from aenum import auto
from geli_python_common.util.constants import CaseInsensitiveEnum

logger = Logger(__name__)


@attr.s
class Subscriptions(ABC):
    """
    Data structure to handle subscriptions for MQTT and AMQP message bus connectors.
    """
    subscriptions = attr.ib(type=dict, init=False, default=attr.Factory(dict))
    default_message_processor = attr.ib(type=Callable, default=None)
    topic_prefix = attr.ib(type=str, default=None)
    topic_separator = None

    def __getitem__(self, item):
        """
        Allow class to be indexed directly to avoid need for indirection <Subscriptions instance>.subscriptions[item] -> <Subscriptions instance>[item]
        :param item: index
        :return: subscription dictionary value for key item
        """
        return self.subscriptions[item]

    def add(self, queue: str, callback: Callable=None, callback_arguments: dict=None, subscription_config: dict=None):
        """
        Add callback subscription for topic.
        :param queue: Queue name
        :param callback: callback function which needs to accept the JSON DTO string as `message` argument and optionally the additionally specified `callback_arguments`
        :param callback_arguments: dictionary of key word arguments passed to the callback function
        :return:
        """

        self.subscriptions[queue] = partial(self._pre_process_message,
                                            callback if callback else self.default_message_processor,
                                            callback_arguments if callback_arguments else {},
                                            subscription_config if subscription_config else {})

    def add_topic(self, topic_elements: Union[list, str], callback: Callable = None, callback_arguments: dict = None,
                  subscription_config: dict = None):
        """
        Add callback subscription for topic.
        :param topic_elements: list of topic elements (["d", "pv", "p", "out"]) or '/'-separated string ("d/pv/p/out")
        :param callback: callback function which needs to accept the JSON DTO string as `message` argument and optionally the additionally specified `callback_argumetns`
        :param callback_arguments: dictionary of key word arguments passed to the callback function
        :param subscription_config:
        :return:
        """
        # add prefix if present
        topic_builder = [self.topic_prefix] if self.topic_prefix else []

        # split string up in components if argument isn't already a list
        topic_elements = topic_elements.split(sep="/") if isinstance(topic_elements, str) else topic_elements

        # attach elements to prefix
        topic_builder.extend(topic_elements)

        # join all together
        topic = self.topic_separator.join(topic_builder)

        self.subscriptions[topic] = partial(self._pre_process_message,
                                            callback if callback else self.default_message_processor,
                                            callback_arguments if callback_arguments else {},
                                            subscription_config if subscription_config else {})

    def add_all(self, subscriptions: 'Subscriptions') -> None:
        if type(subscriptions) != type(self):
            raise ValueError(f'Subscriptions need to be of same type but the existing one is {type(self)} while the new one is {type(subscriptions)}')

        self.subscriptions.update(subscriptions.subscriptions)

    @staticmethod
    def _pre_process_message():
        raise NotImplementedError()


@attr.s
class AmqpSubscriptions(Subscriptions):
    topic_separator = "."

    @staticmethod
    def _pre_process_message(callback, callback_arguments, subscription_config, channel, method_frame, header_frame, body):
        """
        Pre-processor for Pika AMQP library callback signature
        """
        callback(message=body, **callback_arguments)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    @staticmethod
    def convert_topic_to_amqp(topic: str):
        """
        Convert /-separated MQTT topic string to .-separated AMQP identifier.
        """
        return AmqpSubscriptions.topic_separator.join(topic.split(sep="/")) if topic else None


class SubscriptionConfigs(CaseInsensitiveEnum):
    """
    Configuration parameter for individual subscriptions
    """
    DO_NOT_ACK = auto()     # do not acknowledge the message to keep it with the broker / queue