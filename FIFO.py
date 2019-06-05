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
	DL_buffer  = Buffer(2000)
	central_cell = Cell([0, 0],DL_buffer, radius)
	tmp = central_cell.gen_cell()

	plt.figure()
	plt.title("1-1 Topology")
	plt.xlabel('x axis(m)')
	plt.ylabel('y axis(m)')

	plt.plot(tmp[0], tmp[1])   #plot cell

	plt.plot(0, 0, 'r^')

	# create UEs and at the same time create buffers for each UE-------------
	UEs_pos = central_cell.gen_UEs(tmp[0], tmp[1], N_UE)
	plt.plot(UEs_pos[:, 0], UEs_pos[:, 1], "b*")
	plt.show()
	UEs_arr = []
	UEs_buffer = []



	#simulation setup-------------------------------------------
	simulation_T = 100
	loss_bits = {}   #record loss bits for each UE

	latency = {}	#record latency(total latency for all pkt) for each UE
	#initial latency dict
	for ue_id in range(N_UE):
		latency[ue_id] = 0



	#-calculate pkt loss and latancy for each UEs------------------------------
	gen = Traffic_generator(N_UE)



    # do FIFO
	b = central_cell.GetBuffer()


	for t in range(simulation_T):
		UEs_capacity = central_cell.UEs_throughput(cell_bandwidth=10 * 10 ** 6, AllCells_pos=BS_pos)  #(bit)

		UEs_budget = UEs_capacity

		print("At", t,"UEs_budget", UEs_budget)



		#generator generate pkt and send to BS
		gen.generate(t)
		b.enqueue(gen.randSend(), current_time=t)



		#BS send pkt in buffer to UEs
		nextpkt = b[-1]
		print("At", t, "nextpkt", nextpkt)

		if nextpkt == None:  # In this round(sec), no pkt in buffer
			continue

		nextpkt_dest = b[-1].getToWhom()


		while CanSend(b[-1] , budget=UEs_budget[nextpkt_dest]) and nextpkt != None:
			UEs_budget[nextpkt_dest] -= b[-1].getLength()

			ltcy = (b.dequeue()).RecordLatency(t)  #Neglect propagation delay for the sake of simplicity

			#record latency for all sent pkts
			latency[nextpkt_dest] += ltcy


			nextpkt = b[-1]


			if nextpkt == None:  # At this moment in some round, no remaining pkt pkts in buffer.

				break

			nextpkt_dest = b[-1].getToWhom()






	#record loss bits for each UE-------------------------

	for ue in b.getDrop_log():
		loss_bits[ue] = total_bits(b.getDrop_log()[ue])

	print("loss_bits", loss_bits)

	
	print('latency', latency)


	for i in range(N_UE):
		latency[i] = latency[i] / gen.getLog()[i]
	print("latancy per bit", latency)




if __name__ == '__main__':
    main()
