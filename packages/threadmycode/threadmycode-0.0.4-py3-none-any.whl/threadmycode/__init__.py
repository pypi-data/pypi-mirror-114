from threading import Thread, active_count
from typing import Iterable
import time
import os
import logging
from sys import exit as sysexit
from os import _exit as osexit

config = {'STOP':False,'KILLALL':False}

def stop(self, cls):
    logging.info('Stop Signal Recieved')
    global config
    config['STOP'] = True
    return

def killall(self, cls):
    logging.info('kill All Signal Recieved')
    try:
        sysexit(0)
    except SystemExit:
        osexit(0)
          
def threadCount(count):
    config['threadCount'] = count
    return 

def threadit(func):
    global config
    def wrapper(*args,**kwargs):
        if isinstance(args[0],Iterable):
            def proc():
                return "Processed"
            threads = []
            maxThread = config.get('threadCount')
            if maxThread is None:
                maxThread = os.cpu_count() + 1
            if maxThread<=3:
                maxThread = 3
            if maxThread>(os.cpu_count() * 10):
                maxThread = os.cpu_count() * 10
            logging.info('maxthread is' + str(maxThread))
            for elem in args[0]:
                if config['STOP']:
                    break
                while True:
                    activecount = active_count()
                    if (activecount>=maxThread):
                        time.sleep(1)
                    else:
                        break
                logging.info('active count is' + str(activecount))
                newArgs = (elem,) + args[1:]
                if (activecount<maxThread):
                    t1 = Thread(target = func, args =newArgs,kwargs=kwargs)
                    t1.start()
                    logging.info('thread Created with func ' + str(func) + ' args ' + str(newArgs) + ' kwargs ' + str(kwargs))
                    threads.append(t1)
            for thread in threads:
                thread.join()
            return proc
        else:
            x=func(*args,**kwargs)
            return x
    return wrapper

