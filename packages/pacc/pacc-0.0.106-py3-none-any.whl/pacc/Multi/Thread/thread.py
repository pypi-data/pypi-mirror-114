import threading

threadLock = threading.Lock()


def runThread(functionName, args):
	t = threading.Thread(target=functionName, args=args)
	t.start()
	return t
