# Persistent LRU caches



## Redis as LRU cache

https://redis.io/

### Pros

1. Super fast inserts/updates
1. Horizontally scalable
1. HA variant with sentinel (checked, https://redis.io/docs/management/sentinel/)
1. Experience - high (use it in prod for long time)

### Cons

1. Key eviction algorithm is not exact (sometimes not evicts LRU item: https://redis.io/docs/reference/eviction/)
1. Key eviction algoritmh sometimes evicts multiple values when not needed (see/run `check_redis.py`)
1. Not fully configurable (# of keys vs. maxmem value)
1. Need Redis 7 (older versions seems to be broken)
1. Backups etc. - not managed



## Memcached

https://memcached.org/

### Pros

1. Eviction mechanisms
1. Horizontally scalable
1. Easy to deploy and configure

### Cons

1. Slow inserts
1. A bit slower gets
1. Backups etc. - not managed



## Infinispan as LRU cache

https://infinispan.org/

### Pros

1. Resilient
1. HA variant
1. RH product

### Cons

1. Python client/connector is super outdated and broken (very hard to even build it)
1. Python client is not maintained: "This client is currently unmaintained and supports a very limited subset of Hot Rod features."
1. Dunno about official support (just JVM seems to be maintained)
1. Experience - low



## PostgreSQL as LRU cache

https://www.postgresql.org/

### Pros

1. Supported internally
1. Scalable (HA variant)
1. Possible to use RDS if needed
1. Queries as fast as in Redis
1. Very mature Python client
1. Experience - high (use it in prod for long time)
1. Supported (RDS et al)

### Cons

1. Inserts/updates much slower than in Redis
1. LRU eviction need to be explicitly written (as trigger when needed)



## SQLite as LRU cache

https://www.sqlite.org/index.html

### Pros

1. No dependencies (part of Python base packages)
1. Fastest GET operation
1. Suppport? Would it be needed in this situation where it "is in Python"
1. Experience - high

### Cons

1. Super slow inserts/updates (file locks? very inefficient)
1. Not HA or resilient
1. Technically DB w/o schema (the schema is not forced)



## Other possibilities

* Couchbase: document, key-value
    - no LRU
    - no support
    - no experience
* MongoDB: document open source
    - no LRU
    - no support
    - no experience
* NATS: key-value, (internal DB)
    - no LRU
    - no support
    - no experience
* Amazon DynamoDBdocument: key-value
    +- vendored
    + experience



## Benchmark results

```
Postgres cache
----------------------------------------
10000 inserts/appends performed in 75 seconds
132 operations per second

100000 gets performed in 1 seconds
60235 operations per second



SQLite cache
----------------------------------------
10000 inserts/appends performed in 193 seconds
51 operations per second

100000 gets performed in 0 seconds
285370 operations per second



Redis cache
----------------------------------------
10000 inserts/appends performed in 0 seconds
27385 operations per second

100000 gets performed in 1 seconds
62017 operations per second



Memcached cache
----------------------------------------
10000 inserts/appends performed in 408 seconds
24 operations per second

100000 gets performed in 2 seconds
35212 operations per second
```

