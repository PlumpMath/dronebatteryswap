
from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Thread,Lock
import os
from time import sleep
import pdb

'''
This won't run it is just a template



client does:

import xmlrpclib
server = xmlrplib.ServerProx('http://IP:port')
server.yourfct
'''


#Allows for synchronization for Signal variable
GIL = Lock()
#what the signal currently is
Signal = None

#handlers signals
#called by remote raspberry pi over TCP?
class SignalHanler(object):
    global GIL

    #signal to go to A
    def swapToA(self,*args,**kwargs):
        global Signal
        GIL.acquire()
        Signal = 'A'
        GIL.release()
    #signal to go to B
    def swapToB(self, *args,**kwargs):
        global Signal
        GIL.acquire()
        Signal = 'B'
        GIL.release()



def routineB(*args,**kwargs):
    global GIL
    global Signal
    #signals if finished with no signal
    Done = False
    while True:
        print 'B'
        #run something
        #lock the Signal
        GIL.acquire()

    	if Signal == 'A' or Done:
    		Signal = None if Done else 'A'
    		GIL.release()
    		yield
        else:
            GIL.release()
        #you don't need this
        sleep(1)

#same code as routine B
def routineA(*args,**kwargs):
    global GIL
    global Signal
    Done = False
    while True:
        print 'A'
        #run something
        #Done might become True
        GIL.acquire()
        print Signal
        if Signal == 'B' or Done:
            Signal = None if Done else 'B'
            GIL.release()
            yield
        else:
            GIL.release()
        #you don't need this
        sleep(1)

if __name__ == "__main__":
    #get server (ip,port), else default to (127.0.0.1,9000)
    #from env vars
    serveraddress = os.getenv('SERVER_IP','127.0.0.1')
    serverport = os.getenv('SERVER_PORT',9000)
    #instance for handler
    handler = SignalHanler()
    #set up RPC
    server = SimpleXMLRPCServer(
            (serveraddress,serverport),
            logRequests = True,
            allow_none = True
    )
    #register handler
    server.register_instance(handler)
    #start server async thread
    serverThread = Thread(target=server.serve_forever,args=())
    serverThread.start()

    #start with routine A
    Signal = 'A'
    A = routineA()
    B = None
    while True:
        #lock the signal
        GIL.acquire()
        # if told to go to A
        if Signal == 'A':
            #go to A
            GIL.release()
            A.next()
        elif Signal == 'B':
            #if B has never gone before
            if not B:
                GIL.release()
                #intialize and start it
                B = routineB()
            else:
                GIL.release()
                #go to B
                B.next()
        else:
            GIL.release()
            #else if told to do nothing, just sleep and await next signal
            sleep(2)
