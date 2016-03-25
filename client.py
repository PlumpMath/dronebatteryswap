
import xmlrpclib
from time import sleep

server = xmlrpclib.ServerProxy('http://127.0.0.1:9000')

while True:
    print 'Signaling A'
    server.swapToA()
    sleep(2)
    print'Signaling B'
    server.swapToB()
    sleep(2)
