import random
import numpy as np
from datetime import *

class Packet:
    def __init__(self, ToWhom, deadline=3): #suppose default deadline is 3 sec

        self.ToWhom = ToWhom

        length = random.randint(64*8, 1518*8)
        self.length = length

        self.deadline = deadline

        #priority = random.randint(0,7)
        priority = ToWhom   #For the sake of simplicity
        self.priority = priority


    def getDeadline(self):
        return self.deadline
    def getToWhom(self):

        return self.ToWhom

    def	getLength(self):
        return self.length

    def getPriority(self):
        return self.priority





def total_bits(packets):
    '''
    packets: (list) list of pkt objs.
    '''
    total_bits = 0
    for pkt in packets:
        total_bits += pkt.getLength()
    return total_bits





class Traffic_generator():
    def __init__(self, UEs_num):
        self.UEs_num = UEs_num

        self.log = [0] * UEs_num   #record total number of bits have generated for each UE.
                                     #Ex: self.log=[300, 400] which mean there are 300 and 400 bits have generated\
                                           #for UE0 and UE1 respectively to date.

    def generate(self):
        pkt_num = []
        self.traffic = {}

        pkt_num  = np.random.randint(0, 5, self.UEs_num)
            #If UEs_num==3, pkt_num==[5,5,5] which means their number of packets arrived is 5 at this moment(sec)

        for UE_id in range(self.UEs_num):
            pkt_storage = [] #store pkts
            self.traffic[UE_id] = pkt_storage
            for  i in range(pkt_num[UE_id]):  #pkt_num[UE_id]->The number of generated pkts(random length of each pkt) for UE(id=UE_id).
                self.traffic[UE_id].append(Packet(UE_id))

            
            self.log[UE_id] += total_bits(self.traffic[UE_id])


            return self.traffic #{0:[Packet(0),Packet(0)]} represent there are two pkt generated for UE0 at this moment.

    def randSend(self):

        print("original:", self.traffic.values())
        random.shiffle(self.traffic.values())
        print("After:", self.traffic.values())

        return randsend





class Queue:
    def __init__(self, capacity):
        self.buffer = [] #store pkt which would contain random length data
        self.capacity = capacity #total length(bit) which the Queue can accommodate

    def isEmpty(self):
        return self.buffer == []

    def enqueue(self, item):

        self.buffer.insert(0,item)

    def dequeue(self):
        return self.buffer.pop()

    def isoverflow(self):
        size = 0

        for i in range(len(self.buffer)):
            print(self.buffer[i])
            print(type(self.buffer[i]))
            size += self.buffer[i].size()

        return size > self.capacity






def main():
    '''
	u1 = Queue(10)
	p1 = Packet('1', 11, 'nick')
	u1.enqueue(p1)
	users_buffer = []
	users_buffer.insert(0,u1)
	print(u1.isoverflow())
    '''

    gen = Traffic_generator(2)
    print(gen.generate())



if __name__ == '__main__':
    main()
