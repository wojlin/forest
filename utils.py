import requests


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Fetcher(metaclass=SingletonMeta):

    def __init__(self):
        self.requests_done = 0

    def get(self, url: str, good_status: int = 200):
        self.requests_done += 1
        request = requests.get(url)
        if not request.status_code == good_status:
            raise ConnectionError(f"request \"{url}\" returned status code \"{request.status_code}\"")

        return json.loads(request.content)

    @staticmethod
    def print(json_data: dict):
        print(json.dumps(json_data, indent=4))