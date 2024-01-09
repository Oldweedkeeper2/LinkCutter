from environs import Env

env = Env()
env.read_env()

ALCHEMY_DATABASE_URL: str = env.str("ALCHEMY_DATABASE_URL")
DOMAIN_NAME: str = env.str("DOMAIN_NAME")
REDIS: str = env.str("REDIS")

CACHE_TYPE: str = "redis" if REDIS == "redis" else "memcached"
if CACHE_TYPE == "redis":
    CACHE_REDIS_URL: str = env.str("CACHE_REDIS_URL")
