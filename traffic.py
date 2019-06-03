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
        self.buffer.append(item)

    def dequeue(self):
        self.buffer.reverse()
        self.buffer.pop()
        self.buffer.reverse()

    def isoverflow(self):
        size = 0

        for i in range(len(self.buffer)):
            print(self.buffer[i])
            print(type(self.buffer[i]))
            size += self.buffer[i].size()

        return size > self.capacity

    def showstatus(self): 
        for i in range(len(self.buffer)):
            print(self.buffer[i])


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

if __name__ == '__main__':
    main()
