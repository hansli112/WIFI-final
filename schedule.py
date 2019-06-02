# there are several scheduling policy can choose below
# the input is the buffer(queue) that we want to send one of packet within
# the return value is the index of packet to be sent, so you might need to sent the packet by yourself
# the return value is -1 if the buffer is empty
import traffic
from datetime import *

class Schedule:
	nextRR = 0 # the next sending index of priority in round-robin

	def FIFO (buf):
		if buf.isEmpty():
			return -1
		return (len(buf) - 1)

	def RR (buf, numPriority): # please input the buf and how many priority levels we have
		if buf.isEmpty():
			return -1

		while True:
			for i in range(len(buf)):
				if buf[i].priority == nextRR:
					nextRR = (nextRR + 1) % numPriority
					return i
			nextRR = (nextRR + 1) % numPriority # try next possible index since no packet with current index in the buffer
	
	def EDF (buf):
		if buf.Empty():
			return -1

		now = datetime.now()
		index = 0
		minExpire = buf[index].deadline - now # it should be a timedelta object
		for i in range(1, len(buf)): # looking for the packet with earlist deadline
			if buf[i].deadline - now < minExpire:
				minExpire = buf[i].deadline - now # it should be a timedelta object
				index = i
		return index

	def SJF (buf):
		if buf.Empty():
			return -1
		
		index = 0
		minLength = buf[index].length
		for i in range(1, len(buf)): # looking for the job with shortest length
			if buf[i].length < minLength:
				minLength = buf[i].length
				index = i
		return index
