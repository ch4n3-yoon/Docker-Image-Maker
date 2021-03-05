import random
import string


class Api:
    def __init__(self):
        pass

    @staticmethod
    def get_random_string(length: int) -> str:
        dummy = string.ascii_lowercase + string.digits
        return ''.join([random.choice(dummy) for _ in range(length)])


API = Api()
