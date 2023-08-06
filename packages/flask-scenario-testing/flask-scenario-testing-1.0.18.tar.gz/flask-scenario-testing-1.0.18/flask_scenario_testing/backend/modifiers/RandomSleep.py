from flask_scenario_testing.backend.modifiers.Modifier import Modifier
from time import sleep
import random


class RandomSleep(Modifier):
    def identifier(self):
        return 'RANDOM_SLEEP'

    def modify(self, fun, endpoint_name, modifier_args: dict):
        def wrapper(*args, **kwargs):
            base_sleep_ms = int(modifier_args.get('time'))
            random_offset_ms = random.randint(-200, +200)

            sleep_ms = base_sleep_ms + random_offset_ms

            print('Sleeping for {}ms + {}ms = {}ms'.format(base_sleep_ms, random_offset_ms, sleep_ms))
            sleep(sleep_ms / 1000)

            return fun(*args, **kwargs)

        return wrapper
