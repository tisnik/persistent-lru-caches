import random
import time
import uuid

from postgres_cache import PostgresCache
from sqlite_cache import SQLiteCache
from redis_cache import RedisCache
from memcached_cache import MemcacheCache


def gen_keys(conversations):
    return [str(uuid.uuid4()) for i in range(conversations)]


def print_per_second(operations, t1, t2):
    per_second = int(operations / (t2-t1))
    print(f"{per_second} operations per second\n")


def benchmark_insert_or_append(cache, keys, append_count):
    t1 = time.perf_counter()
    for i in range(append_count):
        key = random.choice(keys)
        cache.insert_or_append(key, "* value *")
    t2 = time.perf_counter()
    t = int(t2-t1)
    print(f"{append_count} inserts/appends performed in {t} seconds")
    print_per_second(append_count, t1, t2)


def benchmark_get(cache, keys, get_count):
    t1 = time.perf_counter()
    for i in range(get_count):
        key = random.choice(keys)
        cache.get(key)
    t2 = time.perf_counter()
    t = int(t2-t1)
    print(f"{get_count} gets performed in {t} seconds")
    print_per_second(get_count, t1, t2)


def print_title(title):
    print(title)
    print("-" * 40)

def benchmark_postgres_cache(cache_limit, conversations, append_count, get_count):
    print_title("Postgres cache")
    cache = PostgresCache("dbname=test1 user=ptisnovs password=123qwe", capacity=cache_limit)

    keys = gen_keys(conversations)
    benchmark_insert_or_append(cache, keys, append_count)
    benchmark_get(cache, keys, get_count)


def benchmark_sqlite_cache(cache_limit, conversations, append_count, get_count):
    print_title("SQLite cache")
    cache = SQLiteCache("test.db", capacity=cache_limit)

    keys = gen_keys(conversations)
    benchmark_insert_or_append(cache, keys, append_count)
    benchmark_get(cache, keys, get_count)


def benchmark_redis_cache(cache_limit, conversations, append_count, get_count):
    print_title("Redis cache")
    cache = RedisCache()

    keys = gen_keys(conversations)
    benchmark_insert_or_append(cache, keys, append_count)
    benchmark_get(cache, keys, get_count)


def benchmark_memcached_cache(cache_limit, conversations, append_count, get_count):
    print_title("Memcached cache")
    cache = MemcacheCache()

    keys = gen_keys(conversations)
    benchmark_insert_or_append(cache, keys, append_count)
    benchmark_get(cache, keys, get_count)


# benchmark settings
cache_limit = 500
conversations = 1000
append_count = 10000
get_count = 100000

#benchmark_postgres_cache(cache_limit, conversations, append_count, get_count)
print()
print()
#benchmark_redis_cache(cache_limit, conversations, append_count, get_count)
print()
print()
#benchmark_sqlite_cache(cache_limit, conversations, append_count, get_count)
print()
print()
benchmark_memcached_cache(cache_limit, conversations, append_count, get_count)
