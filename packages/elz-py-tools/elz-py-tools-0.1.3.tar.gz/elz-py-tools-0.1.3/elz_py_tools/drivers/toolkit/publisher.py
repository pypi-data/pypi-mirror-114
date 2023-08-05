import json
import uuid
import logging
import datetime


LOGGER = logging.getLogger(__name__)


class AbstractPublisher(object):
    """ Base class for a amqp message publisher """

    def __init__(self, amqp_driver, sender_id: str):
        self._amqp_driver = amqp_driver
        self._sender_id = sender_id

    async def publish(self, command, body, options={}, expect_response=True):
        """ Publish a message through amqp bus
            if expect_response is True, publish a RPC message and await for response
        """

        # Synaptix format for querying graph or index, perhaps allow other format ?
        message = {
            "headers": {
                "command": command,
                "sender": self._sender_id or uuid.uuid4(),
                "date": datetime.datetime.now().timestamp(),
                **options
            },
            "body": body
        }

        if expect_response:
            response = await self._amqp_driver.request(command, message)

            response = json.loads(response) if type(response) == str else response

            if response["headers"]["status"] == 'OK':
                return response["body"]
            elif response["headers"]["status"] == 'ERROR':
                LOGGER.error(f'An error occurred on processing message : {body}')
                raise Exception(f'Error on message : {response["body"]["errorMessage"]}')

            raise Exception(f'Response with unhandled status : {response}')
        else:
            await self._amqp_driver.publish(command, message)
