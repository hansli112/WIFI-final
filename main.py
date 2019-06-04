from cell import *
import matplotlib.pyplot as plt
from matplotlib import path
import numpy as np
from traffic import *
from channel import *
from schedule import *

#from channel import two_ray_model, ith_SINR, rx_Power, SIN
def main():
	#setup
	temperature = 27 + 273.15  # degree Kelvin
	thermal_noise_p = (1.38 * 10 ** (-23)) * temperature * 10 * (10 ** 6)
	BS_power = 33 - 30  #convert to dB
	UE_power = 0 - 30
	h_BS = 1.5 + 50
	h_UE = 1.5
	BS_gain = 14
	UE_gain = 14
	N_UE = 10   #There are N_UE uniformly distributed in each cell
	ISD = 500   #inter-site distance
	radius = 500 / 3**0.5

	BS_pos = [[0, 0], [0, 500], [0, 1000], [0, -500], [0, -1000],
				   [750 / 3 ** 0.5, 250], [750 / 3 ** 0.5, 750], [750 / 3 ** 0.5, -250], [750 / 3 ** 0.5, -750],
				   [1500 / 3 ** 0.5, 0], [1500 / 3 ** 0.5, 500], [1500 / 3 ** 0.5, -500],
				   [-750 / 3 ** 0.5, 250], [-750 / 3 ** 0.5, 750], [-750 / 3 ** 0.5, -250], [-750 / 3 ** 0.5, -750],
				   [-1500 / 3 ** 0.5, 0], [-1500 / 3 ** 0.5, 500], [-1500 / 3 ** 0.5, -500]]


	BS_pos = np.array(BS_pos)


	# role setup(DL)
	h_t = h_BS
	h_r = h_UE
	tx_power = BS_power
	tx_gain = BS_gain
	rx_gain = UE_gain

#-----print Topology-----------------------------------

	#install DL buffer for cell
	DL_buffer  = Buffer(20)
	central_cell = Cell([0, 0],DL_buffer, radius)
	tmp = central_cell.gen_cell()

	plt.figure()
	plt.title("1-1 Topology")
	plt.xlabel('x axis(m)')
	plt.ylabel('y axis(m)')

	plt.plot(tmp[0], tmp[1])   #plot cell

	plt.plot(0, 0, 'r^')

	# create UEs and at the same time create buffers for each UE
	UEs_pos = central_cell.gen_UEs(tmp[0], tmp[1], N_UE)
	plt.plot(UEs_pos[:, 0], UEs_pos[:, 1], "b*")
	plt.show()
	UEs_arr = []
	UEs_buffer = []



	#simulation setup
	simulation_T = 1000

	print("@@thpt", central_cell.UEs_throughput(cell_bandwidth=10 * 10 ** 6, AllCells_pos=BS_pos))



	#calculate pkt loss
	gen = Traffic_generator(N_UE)

	UEs_capacity = central_cell.UEs_throughput(cell_bandwidth=10 * 10 ** 3, AllCells_pos=BS_pos)  #(bit)

    # do FIFO
	b = central_cell.GetBuffer()

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


	#record loss bits for each UE
	loss_bits = {}
	for ue in b.getDrop_log():
		loss_bits[ue] = total_bits(b.getDrop_log()[ue])

	print("loss_bits", loss_bits)


	'''
	for i  in range(len(UEs_pos)):
		UEs_arr.append(UE(UEs_pos[i], 0, i, i))  #currently assume priority = ID
		UEs_buffer.append(Queue(buffer_size // N_UE))

	'''





if __name__ == '__main__':
    main()
