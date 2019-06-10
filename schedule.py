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

	def FIFO (self, buf):
		if buf.isEmpty():
			return -1


		return buf[-1]


	def RR (self, buf, numPriority): # please input the buf and how many priority levels we have
		if buf.isEmpty():
			return -1

		while True:
			for i in range(len(buf)):
				if buf[-1-i].getPriority() == self.nextRR:
					self.nextRR = (self.nextRR + 1) % numPriority

					return buf[i]   #return next sending pkt
				else:
					self.nextRR = (self.nextRR + 1) % numPriority # try next possible index since no packet with current index in the buffer



	def EDF (self, buf, current_time):
		#return (outputpkt) which pkt obj is the urgentest

		if buf.isEmpty():
			return None

		minExpire = current_time - buf[-1].getTimestamp()
		outputpkt = buf[-1]

		for pkt in buf.ViewBuffer()[::-1]:#reverse list for good processing in ED

			if (current_time - pkt.getTimestamp()) <  minExpire:
				minExpire = current_time - pkt.getTimestamp()
				output = pkt

		return outputpkt



	def SJF (self, buf):
		if buf.isEmpty():
			return -1

		index = 0
		minLength = buf[index].getLength()
		for i in range(len(buf)): # looking for the job with shortest length
			if buf[-1-i].length < minLength:
				minLength = buf[i].getLength()
				index = i

		return buf[index]



def main():


	gen = Traffic_generator(3)
	UEs_capacity = np.array([1e5, 1e5, 1e5])  #()

    # do FIFO
	b = Buffer(7)

	for t in range(10):  #simulation time = 3 sec
		print("@@generate pkts at", t, gen.generate())
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






if __name__ == '__main__':
    main()
