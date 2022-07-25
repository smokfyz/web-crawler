import os

MAX_NESTING_LIMIT = int(os.getenv("MAX_NESTING_LIMIT", 3))

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
