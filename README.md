# Persistent LRU caches

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
