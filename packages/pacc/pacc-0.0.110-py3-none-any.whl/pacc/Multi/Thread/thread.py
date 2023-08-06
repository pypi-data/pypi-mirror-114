import threading
from ...tools import sleep

threadLock = threading.Lock()


def runThread(functionName, args, delay=1):
	sleep(delay)
	t = threading.Thread(target=functionName, args=args)
	t.start()
	return t
