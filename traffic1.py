import random
import numpy as np
from datetime import *

class Packet:
    def __init__(self, ToWhom): #suppose default deadline is 3 sec

        self.ToWhom = ToWhom

        self.length = random.randint(64*8, 1518*8)

        self.deadline = random.randint(100, 3600)

        #priority = random.randint(0,7)
        '''priority = ToWhom   #For the sake of simplicity'''
        self.priority = random.randint(0, 5)

    def __str__(self):
        return "Packet(dest=" + str(self.ToWhom)  + ")"


    def getDeadline(self):
        return self.deadline

    #decrease the time to live of packet
    def decrease_TTL(self):
        self.deadline -= 1

    def getToWhom(self):

        return self.ToWhom

    def	getLength(self):
        return self.length

    def getPriority(self):
        return self.priority


        #show the status of packet
    def show_status(self):
        print("Deadline", self.deadline)
        print("Length", self.length)
        print("Priority", self.priority)
        print("ToWhom", self.ToWhom)





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
        print(pkt_num)
            #If UEs_num==3, pkt_num==[5,5,5] which means their number of packets arrived is 5 at this moment(sec)

        for UE_id in range(self.UEs_num):
            pkt_storage = [] #store pkts
            self.traffic[UE_id] = pkt_storage


            for  i in range(pkt_num[UE_id]):  #pkt_num[UE_id]->The number of generated pkts(random length of each pkt) for UE(id=UE_id).

                self.traffic[UE_id].append(Packet(UE_id))


            self.log[UE_id] += total_bits(self.traffic[UE_id])


        return self.traffic #{0:[Packet(0),Packet(0)]} represent there are two pkt generated for UE0 at this moment.

    def randSend(self):
        #the arrival pattern(from the perspective of buffer) for each arrival round
        traffic_values = [j for i in self.traffic.values() for j in i]

        #the following prove that the order of arrival pkt is random
        '''
        for i in traffic_values:
            print(i)

            print("------------------")


        random.shuffle(traffic_values)
        for i in traffic_values:
            print(i)
            print("------------------")
        '''






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


    packet_1 = Packet("user8")
    packet_1.show_status()
    packet_1.decrease_TTL()
    packet_1.show_status()
    packet_2 = Packet("user4")
    packet_2.show_status()
    packet_2.decrease_TTL()
    packet_2.show_status()
    '''


    gen = Traffic_generator(3)
    print(gen.generate())
    gen.randSend()



if __name__ == '__main__':
    main()
