"""Implementation of LRU cache based on SQLite."""

import sqlite3


class SQLiteCache():
    """Cache that uses SQLite to store cached values."""

    CREATE_CACHE_TABLE = """
        CREATE TABLE IF NOT EXISTS cache (
            key        text UNIQUE NOT NULL,
            value      text,
            updated_at timestamp);
        """

    CREATE_INDEX = """
        CREATE INDEX IF NOT EXISTS timestamps
            ON cache (updated_at)
        """

    UPDATE_STATEMENT = """
        UPDATE cache
           SET value=?, updated_at=CURRENT_TIMESTAMP
         WHERE key=?
        """

    INSERT_STATEMENT = """
        INSERT INTO cache(key, value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """

    DELETE_STATEMENT = """
        DELETE FROM cache WHERE key in (SELECT key FROM cache ORDER BY updated_at LIMIT
        """

    def __init__(self, connection_string, capacity=10):
        """Initialize connection to Postgres."""
        self.conn = sqlite3.connect(connection_string)
        self.initialize_cache()
        self.capacity = capacity

    def initialize_cache(self):
        """Initialize cache - clean it up etc."""
        cur = self.conn.cursor()
        try:
            cur.execute(SQLiteCache.CREATE_CACHE_TABLE)
            cur.execute(SQLiteCache.CREATE_INDEX)
            cur.execute("delete from cache")
        except Exception as e:
            print(e)

        cur.close()
        self.conn.commit()

    def get(self, key: str) -> str | None:
        """Get the value associated with the given key.

        Args:
            key: The key for the desired value.

        Returns:
            The value associated with the key, or None if not found.
        """
        cur = self.conn.cursor()
        cur.execute("select value from cache where key=? limit 1", (key,))
        value = cur.fetchone()
        cur.close()
        if value is not None:
            return value[0]
        return None

    def insert_or_append(self, key: str, value: str) -> None:
        """Set the value associated with the given key.

        Args:
            key: The key for the value.
            value: The value to set.
        """
        oldValue = self.get(key)
        if oldValue:
            self._update(key, oldValue + "\n" + value)
        else:
            self._insert(key, value)
            self._cleanup()
        self.conn.commit()

    def _update(self, key: str, value: str) -> None:
        cur = self.conn.cursor()
        cur.execute(SQLiteCache.UPDATE_STATEMENT, (value, key))
        cur.close()

    def _insert(self, key: str, value: str) -> None:
        cur = self.conn.cursor()
        cur.execute(SQLiteCache.INSERT_STATEMENT, (key, value))
        cur.close()

    def _cleanup(self) -> None:
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM cache;")
        count = cur.fetchone()[0]
        limit = count-self.capacity
        if limit > 0:
            cur.execute(f"{SQLiteCache.DELETE_STATEMENT} {count-self.capacity})")
        cur.close()
