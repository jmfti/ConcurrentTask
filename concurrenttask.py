from threading import Semaphore, Thread 

def executeFunction(f, sem, *arguments):
	""" This is the wrapper function """
    if arguments == []:
        f()
    else:
        f(*arguments)
    sem.release()
 
class ConcurrentTask:
    def __init__(self, f):
        self.f = f
        try:
            if ConcurrentTask.sem is None:
                ConcurrentTask.sem = Semaphore(100)	# 100 threads
        except Exception, e:
            ConcurrentTask.sem = Semaphore(100)
 
    def __call__(self, *arguments):
        ConcurrentTask.sem.acquire()
        arg = [self.f, ConcurrentTask.sem]
 
        if arguments != []:
            arg += list(arguments)
 
        t = Thread( target=executeFunction, args=arg)
        t.start()
		

@ConcurrentTask
def foo():
    print threading.activeCount()
    sleep(random.uniform(0, 1))
 
@ConcurrentTask
def bar(arg1, arg2):
    print threading.activeCount(), arg1, arg2
    sleep(random.uniform(0, 2))


def test():
    for i in xrange(1000):
        foo()
        bar(i,i+1)