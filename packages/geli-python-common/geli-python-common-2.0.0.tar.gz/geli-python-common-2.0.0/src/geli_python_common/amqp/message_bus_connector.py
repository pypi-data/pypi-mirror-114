import attr
from abc import ABC, abstractmethod
from logbook import Logger
from typing import Type, List

from geli_python_common.amqp.subscriptions import AmqpSubscriptions, Subscriptions
from geli_python_common.dto.dto import Dto

logger = Logger(__name__)


@attr.s
class Message(ABC):
    """
    Message intended for a message bus.
    :ivar payload: body of the message in form of a Dto
    """
    payload = attr.ib(type=Type[Dto])
    resource = attr.ib(default=None)


@attr.s
class MessageBusConnector(ABC):
    """
    Client class for connecting to a message bus.
    """
    client_id = attr.ib()
    _message_bus_port = attr.ib(type=int, converter=int)
    _message_bus_host = attr.ib(default="127.0.0.1", type=str)
    loop_in_own_thread = attr.ib(default=False, type=bool)
    # subscriptions for all microservices
    _subscriptions = attr.ib(default=attr.Factory(list))
    message_bus_protocol = None
    # subscriptions for kubernetes-service which required special handling this case, so we will fix in later release
    _k8s_subscriptions = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._k8s_subscriptions = self._k8s_subscriptions if self._k8s_subscriptions else AmqpSubscriptions()

    @abstractmethod
    def send_message(self, message: Message) -> None:
        """
        Publish message to message bus
        """
        raise NotImplementedError()

    def subscribe(self, subscriptions: List[Type['Subscription']]) -> None:
        """
        Register callbacks for all microservices subscriptions.
        """
        self._subscriptions.extend(subscriptions)

        # add callbacks for new subscriptions
        for subscription in subscriptions:
            self._register_callback(subscription.target, subscription.callback.callback)

    def k8s_subscribe(self, subscriptions: Type[Subscriptions]) -> None:
        """
        Register callbacks for k8s service subscriptions.
        """
        self._k8s_subscriptions.add_all(subscriptions)

        # add callbacks for new subscriptions
        for subscription, handle in subscriptions.subscriptions.items():
            self._register_callback(subscription, handle)

    def subscribe_single(self, subscription: 'Subscription') -> None:
        """
        Register callbacks for single subscription.
        """
        self._register_callback(subscription.target, subscription.callback.callback)

