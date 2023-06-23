import json
import aiohttp
import logging

AMPLITUDE_KEY = "943fe957a63f74083f968c0ff2f05a9e"


class Amplitude:
    def __init__(self):
        self.api_key = AMPLITUDE_KEY
        self.endpoint = 'https://api2.amplitude.com/2/httpapi'

    async def log(self,
                  user_id: int,
                  event: str,
                  user_properties=None,
                  event_properties=None):
        amp_event = {
            'user_id': user_id,
            'event_type': event,
            'platform': 'Reshator',
        }

        if event_properties is not None:
            amp_event['event_properties'] = event_properties

        if user_properties is not None:
            amp_event['user_properties'] = user_properties

        amp_request = {
            'api_key': self.api_key,
            'events': [
                amp_event,
            ],
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, data=json.dumps(amp_request)) as response:
                return response


amp = Amplitude()

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
