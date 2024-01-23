# Persistent LRU caches



## Redis as LRU cache

### Pros

1. Super fast inserts/updates
1. HA variant with sentinels

### Cons

1. Key eviction algorithm is not exact (sometimes not evicts LRU item)
1. Key eviction algoritmh sometimes evicts multiple values when not needed
1. Not fully configurable (# of keys vs. maxmem value)
1. Need Redis 7 (older versions seems to be broken)
1. Backups etc. - not managed



## PostgreSQL as LRU cache

### Pros

1. Supported internally
1. Scalable (HA variant)
1. Possible to use RDS if needed
1. Queries as fast as in Redis

### Cons

1. Inserts/updates much slower than in Redis
1. LRU eviction need to be explicitly written (as trigger when needed)



## Benchmark results

```
Postgres cache
----------------------------------------
10000 inserts/appends performed in 75 seconds
132 operations per second

100000 gets performed in 1 seconds
60235 operations per second



Redis cache
----------------------------------------
10000 inserts/appends performed in 0 seconds
27385 operations per second

100000 gets performed in 1 seconds
62017 operations per second
```
