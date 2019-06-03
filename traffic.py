#queue for store packet(bits)
import random

class Packet:

    def __init__(self, ToWhom):
        self.deadline = self.gen_random_deadline()
        self.length = self.gen_random_length()
        self.priority = self.gen_random_priority()
        self.ToWhom = ToWhom
    
    #generate the size of packet by random
    def gen_random_length(self):
        max_size = 100
        min_size = 10
        return random.randint(min_size, max_size)

    #generate the deadline of packet by random
    def gen_random_deadline(self):
        max_deadline = 3600
        min_deadline = 100
        return random.randint(min_deadline, max_deadline)

    #generate the priority of packet by random
    def gen_random_priority(self):
        max_priority = 5
        min_priority = 1
        return random.randint(min_priority, max_priority)

    #generate the towhom of packet by random
    def gen_random_towhom(self):
	max_towhom = 50
	min_towhom = 1
	return random.randint(min_towhom, max_towhom)

    #decrease the time to live of packet
    def decrease_TTL(self):
        self.deadline -= 1

    #show the status of packet 
    def show_status(self):
        print("Deadline", self.deadline)
        print("Length", self.length)
        print("Priority", self.priority)
        print("ToWhom", self.ToWhom)

    def getDeadline(self):
        return self.deadline

    def getToWhom(self):

        return self.ToWhom

    def	size(self):
        return self.length

class Queue:
    def __init__(self, capacity):
        self.buffer = [] #store pkt which would contain random length data
        self.capacity = capacity #total length(bit) which the Queue can accommodate

    def isEmpty(self):
        return self.buffer == []

    def enqueue(self, item):
        self.buffer.insert(0, item)

    def dequeue(self):
        self.buffer.pop()

    def isoverflow(self):
        size = 0

        for i in range(len(self.buffer)):
            print(self.buffer[i])
            print(type(self.buffer[i]))
            size += self.buffer[i].size()

        return size > self.capacity

    #show the status of buffer
    def show_status(self): 
        for i in range(len(self.buffer)):
            print(self.buffer[i])

    #find the position of packet in the buffer
    def show_packet_position(self, packet_id):
        return self.buffer.index(packet_id)

    #check the buffer, if the packet can't be sended, drop it 
    #def if_drop_packet(self, packet_id, packet_TTL):


def main():
    """
	u1 = Queue(10)
	p1 = Packet('nick')
	u1.enqueue(p1)
	users_buffer = []
	users_buffer.insert(0,u1)
	print(u1.isoverflow())
    """
    packet_1 = Packet("user8")
    packet_1.show_status()
    packet_1.decrease_TTL()
    packet_1.show_status()
    packet_2 = Packet("user4")
    packet_2.show_status()
    packet_2.decrease_TTL()
    packet_2.show_status()

if __name__ == '__main__':
    main()
