#!/usr/bin/env python

import matplotlib.pyplot as plt

x = ("Postgres", "SQLite", "Redis", "Memcached")
y = (132, 51, 27385, 24)

plt.figure(1)
plt.title("Inserts/appends per second")
plt.bar(x, y)
plt.savefig("inserts_appends.png")
plt.show()

y = (60235, 285370, 62017, 35212)

plt.figure(1)
plt.title("Gets per second")
plt.bar(x, y)
plt.savefig("gets.png")
plt.show()
