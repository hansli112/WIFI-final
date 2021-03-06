# there are several scheduling policy can choose below
# the input is the buffer(queue) that we want to send one of packet within
# the return value is the index of packet to be sent, so you might need to sent the packet by yourself
# the return value is -1 if the buffer is empty
from traffic import *
from datetime import *

def CanSend(packet, budget):
		'''
		Ex:
		(Assum at each moment, we could send any # of pkt as long as UEs' capacity allows)

		if buffer=[P1,P1],first P1 size=1000(bit), second P1_size=500, UE1's capacity(initial budget)= 1300bit/s
		So, at this moment(sec), after sending P1 to UE1, budget will become 1300-1000, and we can
		find the size of second P1 > budget, so we could not send second P1 at this moment.
		'''
		if packet.getLength() <= budget:
			return True
		return False

class Schedule:
	def __init__(self):
		self.nextRR = 0 # the next sending index of priority in round-robin

		self.numPriority = 8 # set the number of quantums
		self.quantum = (8, 7, 6, 5, 4, 3, 2, 1) # set the quantum of each queue manually
		self.nextMultiLevel = 0
		self.nextProcessed = 0 # the next processed task of current priority

	def FIFO (self, buf, *arg):
		if buf.isEmpty():
			return -1
		return buf[-1]

	def RR (self, buf, *numPriority): # please input the buf and how many priority levels we have
		numPriority =  numPriority[0]		#handle tuple input type in *numPriority

		if buf.isEmpty():
			return -1

		while True:
			for i in range(len(buf)):
				if buf[-1-i].getPriority() == self.nextRR:
					self.nextRR = (self.nextRR + 1) % numPriority
					return buf[-1-i]   #return next sending pkt
			
			self.nextRR = (self.nextRR + 1) % numPriority# try next possible index since no packet with current index in the buffer

	def EDF (self, buf, *current_time):
		#return (outputpkt) which pkt obj is the urgentest


		current_time =  current_time[0]			#handle tuple input type in *current_time


		if buf.isEmpty():
			return None

		minExpire = buf[-1].getDeadline() - (current_time - buf[-1].getTimestamp())
		outputpkt = buf[-1]

		for pkt in buf.ViewBuffer()[::-1]:#reverse list for good processing in ED
			if (pkt.getDeadline() - (current_time - pkt.getTimestamp())) <  minExpire:
				minExpire = pkt.getDeadline() - (current_time - pkt.getTimestamp())
				output = pkt
		return outputpkt

	def SJF (self, buf, *arg):
		if buf.isEmpty():
			return -1

		index = 0
		minLength = buf[index].getLength()

		for i in range(len(buf)): # looking for the job with shortest length
			if buf[-1-i].length < minLength:
				minLength = buf[-1-i].getLength()
				index = i
		return buf[-1-index]

	def multi_queue(self, buf, *arg):
		if buf.isEmpty():
			return -1

		for i in range(self.numPriority):
			for j in range(len(buf)):
				if buf[-1-j].priority == self.nextMultiLevel:
					if self.nextProcessed < self.quantum[self.nextMultiLevel]:
						self.nextProcessed += 1
					else:
						self.nextMultiLevel = (self.nextMultiLevel + 1) % self.numPriority
						self.nextProcessed = 0
					return buf[-1-j]
			# if there is no any packet with current priority, looking for next priority
			self.nextMultiLevel = (self.nextMultiLevel + 1) % self.numPriority
			self.nextProcessed = 0








def main():

	'''
	gen = Traffic_generator(3)
	UEs_capacity = np.array([1e5, 1e5, 1e5])  #()

    # do FIFO
	b = Buffer(7)

	for t in range(10):  #simulation time = 3 sec
		print("@@generate pkts at", t, gen.generate(t))
		b.enqueue(gen.randSend())
		print("b.buffer",b.buffer)

		nextpkt = b[-1]

		if nextpkt == None:  # In this round(sec), no pkt in buffer
			continue

		nextpkt_dest = b[-1].getToWhom()

		while CanSend(b[-1] , UEs_capacity[nextpkt_dest]) and nextpkt != None:
			b.dequeue()
			nextpkt = b[-1]
			if nextpkt == None:  # At this moment in some round, no remaining pkt pkts in buffer.
				break

			nextpkt_dest = b[-1].getToWhom()


	print("viewbuffer", b.ViewBuffer())
	print("getdrop_log",b.getDrop_log())

	'''




if __name__ == '__main__':
    main()
