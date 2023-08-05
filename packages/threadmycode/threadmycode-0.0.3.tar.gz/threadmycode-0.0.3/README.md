**threadmycode** is a tiny Python library lets you convert your Python methods into asynchronous,
non-blocking methods simply by using a decorator.

To enable the theading mode, 
    First paramater should not be keyword paramater
    First paramater of the function must be iterable 
    Function will be called in thread with first paramter as iterated value of iterable

if first paramater is not a iterable then normal execution happens

Example
--------------------
```python

    # example.py
    import threadmycode as multithreading
    import time
    import random
    import signal
    # kill all tasks on ctrl-c
    # signal.signal(signal.SIGINT, multithreading.killall)

    # or, wait for task to finish on ctrl-c:
    signal.signal(signal.SIGINT, multithreading.stop)

    @multithreading.threadit
    def hello(count):
        sleep = 3
        print("Hello %s (sleeping for %ss)" % (count, sleep))
        time.sleep(3)
        print("Goodbye %s (after for %ss)" % (count, sleep))

    if __name__ == "__main__":
            multithreading.threadCount(5)
            hello(range(10))
```

The output would look something like this:


```python
    $ python example.py
    
    Hello 0 (sleeping for 3s)
    Hello 1 (sleeping for 3s)
    Hello 2 (sleeping for 3s)
    Hello 3 (sleeping for 3s)
    Goodbye 0 (after for 3s)
    Goodbye 1 (after for 3s)
    Goodbye 2 (after for 3s)
    Goodbye 3 (after for 3s)
    Hello 4 (sleeping for 3s)
    Hello 5 (sleeping for 3s)
    Hello 6 (sleeping for 3s)
    Hello 7 (sleeping for 3s)
    Goodbye 4 (after for 3s)
    Goodbye 5 (after for 3s)
    Hello 8 (sleeping for 3s)
    Goodbye 6 (after for 3s)
    Hello 9 (sleeping for 3s)
    Goodbye 7 (after for 3s)
    Goodbye 8 (after for 3s)
    Goodbye 9 (after for 3s)
```
Settings
========

The default maximum threads is equal to the # of CPU Cores.
**This is just a rule of thumb!** The ``Thread`` module isn't actually using more than one core at a time.

You can change the default maximum number of threads using:

```python

    import threadmycode as multithreading
    multitasking.threadCount(10)
```
