import random
import numpy as np
from datetime import *

random.seed(0)
np.random.seed(0)

#remove nested list-------------------------------------
def removeNestList(alist):
    output = []
    for i in alist:
        if type(i) is list:
            for j in i:
                output.append(j)

        else:
            output.append(i)
    return output
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
def total_bits(packets):
    #Return total bits of all pkts in a list
    '''
    packets: (list)    list of pkt objs.
    '''
    total_bits = 0
    for pkt in packets:
        total_bits += pkt.getLength()
    return total_bits



#--------------------------------------------------------------------------







class Packet:
    def __init__(self, ToWhom, time_stamp): #suppose default deadline is 3 sec
        '''
        timestamp is the time when the packet is generated;
        '''

        self.ToWhom = ToWhom
        self.priority = ToWhom % 8   #0~7
        self.length = random.randint(64*8, 1518*8)


        self.deadline = 50 #random.randint(1, 5)*(1+self.prioriy) 
        self.time_stamp = time_stamp



    def __str__(self):
        return "Packet(dest=" + str(self.ToWhom)  + ")"


    def getDeadline(self):
        return self.deadline


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


    def RecordLatency(self, arrival_time):
        latency = arrival_time - self.time_stamp

        return latency

    def getTimestamp(self):
        return self.time_stamp















class Traffic_generator():
    def __init__(self, UEs_num):
        self.UEs_num = UEs_num

        self.log = [0] * UEs_num   #record total number of bits have generated for each UE.
                                     #Ex: self.log=[300, 400] which mean there are 300 and 400 bits have generated\
                                           #for UE0 and UE1 respectively to date.

        self.pkt_numLog = [0] * UEs_num

    def generate(self, time_stamp):
        pkt_num = []
        self.traffic = {}

        pkt_num  = np.random.randint(5, 10, self.UEs_num)

            #If UEs_num==3, pkt_num==[5,5,5] which means their number of packets arrived is 5 at this moment(sec)


        for UE_id in range(self.UEs_num):
            pkt_storage = [] #store pkts
            self.traffic[UE_id] = pkt_storage


            for  i in range(pkt_num[UE_id]):  #pkt_num[UE_id]->The number of generated pkts(random length of each pkt) for UE(id=UE_id).

                self.traffic[UE_id].append(Packet(UE_id, time_stamp))


            self.log[UE_id] += total_bits(self.traffic[UE_id])  # record total bits arrival at BS for each UE

            self.pkt_numLog[UE_id] += len(self.traffic[UE_id])

        return self.traffic #{0:[Packet(0),Packet(0)]} represent there are two pkt generated for UE0 at this moment.

    def randSend(self):
        #the arrival pattern(from the perspective of buffer) for each arrival round
        traffic_values = [j for i in self.traffic.values() for j in i]

        #the following prove that the order of arrival pkts is random
        '''
        for i in traffic_values:
            print(i)

            print("------------------")


        random.shuffle(traffic_values)
        for i in traffic_values:
            print(i)
            print("------------------")
        '''

        random.shuffle(traffic_values) #the order of arrival pkt is random

        return traffic_values  #type(traffic_values) is list

    def getLog(self):
        return self.log  #type(self.log) is list

    def get_pkt_numLog(self):
        return self.pkt_numLog



class Buffer:
    def __init__(self, capacity):
        self.buffer = [] #store pkt which would contain random length data
        self.capacity = capacity #total # of pkt objs which the Buffer can accommodate

        self.drop_log = {}




    def __getitem__(self, index):
            if index >= len(self.buffer) or len(self.buffer) == 0:
                return None

            return self.buffer[index]

    def __len__(self):
        return len(self.buffer)

    def ViewBuffer(self):
        return self.buffer



    def isEmpty(self):
        return self.buffer == []

    def enqueue(self, item, current_time):

        self.buffer.insert(0,item)


        self.buffer = removeNestList(self.buffer) #remove nested list
        #print("self.buffer", self.buffer)

        #drop pkts which are expired
        self.deadline_drop(currentT=current_time)

        if self.isoverflow():  #handle event of  buffer overflowing
            self.overflow_drop()



    def dequeue(self, pkt): #"pkt" argument is optional argument

        self.buffer.remove(pkt)
        return pkt



    def isoverflow(self):
        size = 0

        for i in range(len(self.buffer)):
            #print(self.buffer[i])
            #print(type(self.buffer[i]))
            size += self.buffer[i].getLength()

        return size > self.capacity

    def getCapacity(self):

        return self.capacity

    def overflow_drop(self):
        overflowdrop = self.buffer[ : -1-self.capacity + 1]  #list of pkt objs
        del self.buffer[ : -1-self.capacity + 1]  #drop it!

        #update drop_log
        for dropped_pkt in overflowdrop:
            if dropped_pkt.getToWhom() not in self.drop_log:

                self.drop_log[dropped_pkt.getToWhom()] = []

            self.drop_log[dropped_pkt.getToWhom()].append(dropped_pkt)




    def deadline_drop(self, currentT):
        deadlinedrop = []
        #record which pkts are expired
        for pkt in self.buffer:
            if (currentT - pkt.getTimestamp()) > pkt.getDeadline():
                deadlinedrop.append(pkt)
                self.buffer.remove(pkt)    #drop it!


        #update drop_log
        for dropped_pkt in deadlinedrop:
            if dropped_pkt.getToWhom() not in self.drop_log:

                self.drop_log[dropped_pkt.getToWhom()] = []

            self.drop_log[dropped_pkt.getToWhom()].append(dropped_pkt)




    def getDrop_log(self):

        return self.drop_log
























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
