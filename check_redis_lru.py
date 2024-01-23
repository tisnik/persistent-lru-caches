from time import sleep

from redis_cache import RedisCache

keys = [str(i+1) for i in range(20)]


def step1():
    redis = RedisCache("1mb")
    for i in range(500):
        for key in keys:
            redis.insert_or_append(key, "value    ")
        sleep(0.010)
        print(i)

    print("Stored items:")
    for key in keys:
        print(len(redis.get(key)), end="  ")
    print()


def step2():
    redis = RedisCache("1mb")
    for i in range(100000):
        redis.insert_or_append("x", "value    ")
        sleep(0.010)
        for key in keys:
            print(redis.redis_client.exists(key), end=" ")
        print(len(redis.get("x")))


step1()
step2()
