from faker import Faker
from sqlalchemy.orm import sessionmaker
from cacheout import Cache
from .variable_manager import VariableManager


class GlobalVariable(VariableManager):
    db: sessionmaker
    faker: Faker
    cache: Cache
    dns_cache: Cache
    route_cache: Cache

    def __init__(self):
        super().__init__(load_file=True)

        self.init_faker()
        self.init_cache()

        if self.get_conf("SERVER_NAME") is None:
            self.set_conf("SERVER_NAME", "v2ray_subscribe")

    def init_faker(self):
        self.faker = Faker()

    def init_db(self, engine):
        if self.get_conf_bool("ENABLE_DATABASE", default=True):
            self.db = sessionmaker(bind=engine)

    def init_cache(self):
        def new_cache():
            return Cache(
                maxsize=self.get_conf_int("CACHE_MAXSIZE", 256),
                ttl=self.get_conf_float("CACHE_TTL"),
            )

        self.cache = new_cache()
        self.dns_cache = new_cache()
        self.route_cache = new_cache()

    def get_db(self):
        return self.db()

    def get_user_agent(self):
        return self.faker.user_agent()
