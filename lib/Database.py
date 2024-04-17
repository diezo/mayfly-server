from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from pymongo.database import Database as MongoDatabase


class Database(MongoDatabase):

    _instance = None
    initialized: bool = False

    CREDENTIALS: tuple[str, str] = ("admin", "ZS9sLMJx0h6hFvUZ")
    CLUSTER: str = "Main"

    uri: str = (
        f"mongodb+srv://{CREDENTIALS[0]}:{CREDENTIALS[1]}"
        f"@main.9svzlqu.mongodb.net/?retryWrites=true&w=majority&appName=Main"
    )

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self.initialized:
            super().__init__(MongoClient(self.uri, server_api=ServerApi("1")), self.CLUSTER)
            self.initialized = True
