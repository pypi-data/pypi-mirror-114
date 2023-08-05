import threadmycode as multithreading
import time
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