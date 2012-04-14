import OSC
import sys
import time

client = OSC.OSCClient()
for i in range( 0, 10 ):
	msg = OSC.OSCMessage()
	msg.setAddress("/OSC")
	msg.append( "message: " + str(i) )
	time.sleep( 0.2 )
	client.sendto(msg, ('127.0.0.1', 5444)) # note that the second arg is a tupple and not two arguments
