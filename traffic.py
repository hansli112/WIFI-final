#queue for store packet(bits)

class Packet:
    def __init__(self,deadline, length, ToWhom):

        self.deadline = deadline
        self.length = length
        self.ToWhom = ToWhom
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

	u1 = Queue(10)
	p1 = Packet('1', 11, 'nick')
	u1.enqueue(p1)
	users_buffer = []
	users_buffer.insert(0,u1)
	print(u1.isoverflow())

if __name__ == '__main__':
    main()
