import zmq

class zmqToolsLibrary:
	def dealerMessage(self, msgType, msgJson):
		# dealer
		context = zmq.Context()
		dealer = None
		try:
			dealer = context.socket(zmq.DEALER)
			print ("dealer連線...")
			dealer.connect("tcp://localhost:5560")
			print(msgType);
			dealer.send_string(msgJson)
			print(dealer.recv_string())
		finally:
			if( dealer is not None):
				dealer.close()
			if( context is not None):
				context.term()
