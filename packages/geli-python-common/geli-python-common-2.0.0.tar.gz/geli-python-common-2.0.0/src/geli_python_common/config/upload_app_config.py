from datetime import datetime

from logbook import Logger

from geli_python_common.amqp.amqp import AmqpMessage
from geli_python_common.dto.dto import ConfigDto, VersionDto


logger = Logger(__name__)

CONFIG_EXCHANGE = "config"
VERSION_EXCHANGE = "version"


def upload_service_config(config_dict: dict, service: str, identifier: str, routingKey: str,
                          amqp_connector_publish: 'AmqpBlockingConnector') -> None:
    """
    Sends service config information to CTS
    """
    config_dict = {k: v for k, v in config_dict.items() if not (k.startswith('__') and k.endswith('__'))}
    config_dto = ConfigDto(timestamp=datetime.now(), service=service, identifier=identifier, properties=config_dict)

    amqp_connector_publish.send_message(AmqpMessage(exchange=CONFIG_EXCHANGE, routing_key=routingKey,
                                                    payload=config_dto.to_json()))
    logger.info(f'Published the ConfigDto')


def upload_service_version(version: str, service: str, identifier: str, routingKey: str,
                           amqp_connector_publish: 'AmqpBlockingConnector') -> None:
    """
     Sends service version information to CTS
    """
    logger.info(f'{service} version is {version}')

    version_dto = VersionDto(timestamp=datetime.now(), service=service, identifier=identifier, version=version)

    amqp_connector_publish.send_message(AmqpMessage(exchange=VERSION_EXCHANGE, routing_key=routingKey,
                                                    payload=version_dto.to_json()))
    logger.info(f'Published the VersionDto')
