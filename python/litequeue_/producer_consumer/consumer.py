import json
import time

from litequeue import SQLQueue

from models import Task


class Consumer:
    def __init__(self, unlock: bool = False):
        queue = SQLQueue("tasks.sqlite")
        self._queue = queue

        num_total, num_locked, num_done = self.stats
        if num_locked:
            print(f"WARNING: Found {num_locked} locked tasks")
            if unlock:
                print("Unlocking tasks...")
                queue.conn.execute("UPDATE Queue SET status = 0 WHERE status = 1")

    @property
    def stats(self):
        total, locked, done = next(self._queue.conn.execute("""
            SELECT COUNT(*) AS total,
                   sum(case when status = 1 then 1 else 0 end) AS locked,
                   sum(case when status = 2 then 1 else 0 end) as done
            FROM Queue
            """))
        return total, locked, done

    def print_queue(self):
        total, locked, done = self.stats
        print(f"Queue status: {total=}, {locked=}, {done=}")

    def run(self, poll_sec: int = 1):
        while True:
            self.print_queue()
            row = self._queue.pop()
            if row:
                task = Task(**json.loads(row["message"]))
                print(f"Processing {task=}")
                # simulate some processing
                time.sleep(1)
                self._queue.done(row["message_id"])

            time.sleep(poll_sec)
