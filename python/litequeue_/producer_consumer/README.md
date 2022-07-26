This is an example of a Producer/Consumer architecture implemented using the
[`litequeue`](https://litements.exampl.io/queue/) library operating over an
on-disk `sqlite3` database

```
$ python3 run.py
Running server in subprocess (pid=502960)
Queue status: total=0, locked=None, done=None
Queue status: total=0, locked=None, done=None
Queue status: total=0, locked=None, done=None
Sending 5 requests with a pool of 2 processes
Queue status: total=0, locked=None, done=None
Got server reply: {'task_id': '459c6955-3745-4d04-b490-893bc716571e', 'queue_row': 1}
Got server reply: {'task_id': 'e88e85ad-f23c-4cb3-a132-135857a6247d', 'queue_row': 2}
Got server reply: {'task_id': '7c680eba-2579-4607-8f4c-4becd9df57e8', 'queue_row': 3}
Got server reply: {'task_id': '49a719c7-a0fc-40f1-8f09-c45813cd00df', 'queue_row': 4}
Got server reply: {'task_id': '567c12dc-a04a-46f5-9f2d-5c9a5f60a06d', 'queue_row': 5}
Queue status: total=5, locked=0, done=0
Processing task=Task(request=CreateRequest(data=32), task_id='459c6955-3745-4d04-b490-893bc716571e')
Queue status: total=5, locked=0, done=1
Processing task=Task(request=CreateRequest(data=183), task_id='e88e85ad-f23c-4cb3-a132-135857a6247d')
Queue status: total=5, locked=0, done=2
Processing task=Task(request=CreateRequest(data=121), task_id='7c680eba-2579-4607-8f4c-4becd9df57e8')
^CTraceback (most recent call last):
  File "/home/snoopjedi/playground/python/litequeue_/producer_consumer/run.py", line 50, in <module>
    consumer_thread.join()
  File "/home/snoopjedi/.pyenv/versions/3.9.9/lib/python3.9/threading.py", line 1053, in join
    self._wait_for_tstate_lock()
  File "/home/snoopjedi/.pyenv/versions/3.9.9/lib/python3.9/threading.py", line 1073, in _wait_for_tstate_lock
    if lock.acquire(block, timeout):
KeyboardInterrupt

$ # The consumer can recover from the above interrupt, although the task that was running is still locked
$ python3 run.py
WARNING: Found 1 locked tasks
Queue status: total=5, locked=1, done=2
Processing task=Task(request=CreateRequest(data=189), task_id='49a719c7-a0fc-40f1-8f09-c45813cd00df')
Running server in subprocess (pid=503023)
Queue status: total=5, locked=1, done=3
Processing task=Task(request=CreateRequest(data=25), task_id='567c12dc-a04a-46f5-9f2d-5c9a5f60a06d')
Sending 5 requests with a pool of 2 processes
Got server reply: {'task_id': '34b2ed6f-9e51-4f66-a536-6160e72a6ce5', 'queue_row': 9}
Got server reply: {'task_id': '83f1a907-f04f-42ec-8dd7-f68db438ea6a', 'queue_row': 6}
Got server reply: {'task_id': '314d6ace-b2cd-4e5c-b24d-58f7193731b5', 'queue_row': 7}
Got server reply: {'task_id': '1be8506c-7ada-41fc-8278-947a9bc84159', 'queue_row': 8}
Got server reply: {'task_id': '42a61acf-9b0e-46c5-abcb-bb7d5b0428a2', 'queue_row': 10}
Queue status: total=10, locked=1, done=4
Processing task=Task(request=CreateRequest(data=153), task_id='83f1a907-f04f-42ec-8dd7-f68db438ea6a')
Queue status: total=10, locked=1, done=5
Processing task=Task(request=CreateRequest(data=26), task_id='314d6ace-b2cd-4e5c-b24d-58f7193731b5')
Queue status: total=10, locked=1, done=6
Processing task=Task(request=CreateRequest(data=173), task_id='1be8506c-7ada-41fc-8278-947a9bc84159')
^CTraceback (most recent call last):
  File "/home/snoopjedi/playground/python/litequeue_/producer_consumer/run.py", line 50, in <module>
    consumer_thread.join()
  File "/home/snoopjedi/.pyenv/versions/3.9.9/lib/python3.9/threading.py", line 1053, in join
    self._wait_for_tstate_lock()
  File "/home/snoopjedi/.pyenv/versions/3.9.9/lib/python3.9/threading.py", line 1073, in _wait_for_tstate_lock
    if lock.acquire(block, timeout):
KeyboardInterrupt

$ # run once more with unlock-at-init behavior
$ UNLOCK=1 python3 run.py
WARNING: Found 2 locked tasks
Unlocking tasks...
Running server in subprocess (pid=503088)
Queue status: total=10, locked=0, done=6
Processing task=Task(request=CreateRequest(data=121), task_id='7c680eba-2579-4607-8f4c-4becd9df57e8')
Queue status: total=10, locked=0, done=7
Processing task=Task(request=CreateRequest(data=173), task_id='1be8506c-7ada-41fc-8278-947a9bc84159')
Sending 5 requests with a pool of 2 processes
Got server reply: {'task_id': 'd367999c-de66-4d62-996b-91090af31407', 'queue_row': 12}
Got server reply: {'task_id': '3ba67623-f018-45ec-9821-d06c37c83eec', 'queue_row': 11}
Got server reply: {'task_id': '17cdba30-87e1-4a11-8891-43f51e3f3efc', 'queue_row': 13}
Got server reply: {'task_id': 'f89de637-85da-47b2-95cb-110ba94b12e4', 'queue_row': 14}
Got server reply: {'task_id': '84f27336-3913-4df5-9b8e-c8b010de23e7', 'queue_row': 15}
Queue status: total=15, locked=0, done=8
Processing task=Task(request=CreateRequest(data=132), task_id='34b2ed6f-9e51-4f66-a536-6160e72a6ce5')
Queue status: total=15, locked=0, done=9
Processing task=Task(request=CreateRequest(data=236), task_id='42a61acf-9b0e-46c5-abcb-bb7d5b0428a2')
Queue status: total=15, locked=0, done=10
Processing task=Task(request=CreateRequest(data=144), task_id='3ba67623-f018-45ec-9821-d06c37c83eec')
Queue status: total=15, locked=0, done=11
Processing task=Task(request=CreateRequest(data=172), task_id='d367999c-de66-4d62-996b-91090af31407')
Queue status: total=15, locked=0, done=12
Processing task=Task(request=CreateRequest(data=45), task_id='17cdba30-87e1-4a11-8891-43f51e3f3efc')
Queue status: total=15, locked=0, done=13
Processing task=Task(request=CreateRequest(data=248), task_id='f89de637-85da-47b2-95cb-110ba94b12e4')
Queue status: total=15, locked=0, done=14
Processing task=Task(request=CreateRequest(data=58), task_id='84f27336-3913-4df5-9b8e-c8b010de23e7')
Queue status: total=15, locked=0, done=15
Queue status: total=15, locked=0, done=15
Queue status: total=15, locked=0, done=15
...
```
