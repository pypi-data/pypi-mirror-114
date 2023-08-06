import platform
from datetime import datetime, timedelta
from time import sleep
from aenum import Enum

from geli_python_common.database.dbhelper import sqlalchemy_commit
from geli_python_common.amqp.amqp import AmqpBlockingConnector, AmqpMessage

DB_STATUS_KEY = 'db_last_healthy_time'
AMQP_STATUS_KEY = 'amqp_last_healthy_time'
AMQP_HEALTH_ROUTING_KEY = 'request.health'
HEALTHY_THRESHOLD_IN_SECS = 180

class STATUS(Enum):
    UP = 'UP'
    DOWN = 'DOWN'

from logbook import Logger
logger = Logger(__name__)


def db_health_check(session: 'Session', Status: 'Status', healthy_threshold_in_secs: int = HEALTHY_THRESHOLD_IN_SECS):
    """
    Performs the DB health check and returns the status

    :param session: SQLAlchemy session
    :param Status: Status DB object
    :return: return enum STATUS (UP, DOWN)
    """

    # Perform DB health check
    db_status = STATUS.DOWN

    try:

        # Save current time in DB
        time_now = datetime.now()
        status = Status(name=DB_STATUS_KEY, last_healthy=time_now)
        session.merge(status)
        sqlalchemy_commit(session)

        # Retrieve the saved time from DB
        status =  session.query(Status).filter(Status.name == DB_STATUS_KEY).first()

        # Check for the DB health status in the database. If the time elapsed since the last time stored in the DB_STATUS_KEY is
        # less than healthy_threshold_in_secs, flag the health status as UP
        if status is not None and datetime.now() - status.last_healthy < timedelta(seconds=healthy_threshold_in_secs):
            db_status = STATUS.UP

    except Exception as e:
        logger.error(f'Error in db_health_check() - {e}')

    return db_status


def amqp_listener_health_check(exchange: str, message_bus_host: str, message_bus_port: int,
                               username: str, password: str, session: 'Session', Status: 'Status',
                               healthy_threshold_in_secs: int = HEALTHY_THRESHOLD_IN_SECS):

    """
    Performs the AMQP health check and returns the status
    :param exchange: health exchaange name
    :param message_bus_host: AMQP host
    :param message_bus_port: AMQP port
    :param username: AMQP user
    :param password: AMQP password
    :param session: SQLAlchemy session
    :param Status: Status DB object
    :return: return enum STATUS (UP, DOWN)
    """

    amqp_status = STATUS.DOWN

    try:
        # AMQP connection for publisher
        clientid = f'test_health_publisher_{platform.node()}'
        amqp_publisher_conn = AmqpBlockingConnector(client_id=clientid,
                                                    message_bus_host=message_bus_host,
                                                    message_bus_port=message_bus_port,
                                                    username=username,
                                                    password=password)

        amqp_publisher_conn.connect()

        # Publish the health message
        message = AmqpMessage(exchange=exchange,
                              routing_key=AMQP_HEALTH_ROUTING_KEY,
                              payload='health')
        amqp_publisher_conn.send_message(message)

        # Check for the AMQP health status in the database. If the time elapsed since the last time stored in the AMQP_STATUS_KEY is
        # less than healthy_threshold_in_secs, flag the health status as UP
        status = session.query(Status).filter(Status.name == AMQP_STATUS_KEY).first()

        # This happens the first time when a health check is performed, when there is no "last status" stored in the DB
        if status is None:
            status = Status(name=AMQP_STATUS_KEY, last_healthy=datetime.now())
            session.merge(status)
            sqlalchemy_commit(session)

        if status is not None and datetime.now() - status.last_healthy < timedelta(seconds=healthy_threshold_in_secs):
            amqp_status = STATUS.UP

        amqp_publisher_conn.disconnect()
    except Exception as e:
        logger.error(f'Error in db_health_check() - {e}')

    return amqp_status