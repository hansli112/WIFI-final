from cell import *
import matplotlib.pyplot as plt
from matplotlib import path
import numpy as np
from traffic import *
from channel import *
from schedule import *
import matplotlib.pyplot as plt

def score(factor, BER, latency_per_bit):
	#argument BER and latency_per_bit are dict

	metric = factor * np.array(list(BER.values()))+ (1 - factor) * np.array(list(latency_per_bit.values()))



	return 1 - metric / sum(metric)


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


central_cell = Cell([0, 0], radius)

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





def Simulator(algorithm):
	'''
	algorithm: specify which scheduling method.
	'''

	#install buffer for following scheduling algorithm
	central_cell.InstallBuffer()

	#simulation setup-------------------------------------------

	simulation_T = 100
	loss_bits = {}   #record loss bits for each UE
	biterror_rate = {}
	latency = {}	#record latency(total latency for all pkt) for each UE
	#initial latency, BER dict
	for ue_id in range(N_UE):
		latency[ue_id] = 0
		biterror_rate[ue_id] = 0
		loss_bits[ue_id] = 0


	#-calculate pkt loss and latancy for each UEs------------------------------
	gen = Traffic_generator(N_UE)



	b = central_cell.GetBuffer()


	#install scheduler
	scheduler = Schedule()

	for t in range(simulation_T):
		UEs_capacity = central_cell.UEs_throughput(cell_bandwidth=10 * 10 ** 6, AllCells_pos=BS_pos)  #(bit)

		UEs_budget = UEs_capacity




		#generator generate pkt and send to BS
		gen.generate(t)
		b.enqueue(gen.randSend(), current_time=t)



		if b.isEmpty():  # In this round(sec), no pkt in buffer
			continue


		#BS send pkt in buffer to UEs

		methods = [scheduler.FIFO, scheduler.EDF, scheduler.SJF, scheduler.multi_queue, scheduler.RR]

		if algorithm == 'RR':
			arg = 8  		#argument for schedule function is numPriority
		elif algorithm == 'EDF':
			arg = t 		#argument for schedule function is current_time
		else:
			arg = None

		for m in methods:
			if algorithm == m.__name__:
				schedule = m

		nextpkt = schedule(b, arg)



		nextpkt_dest = nextpkt.getToWhom()


		while CanSend(nextpkt , budget=UEs_budget[nextpkt_dest]):
			UEs_budget[nextpkt_dest] -= nextpkt.getLength()

			ltcy = (b.dequeue(pkt=nextpkt)).RecordLatency(t)  #Neglect propagation delay for the sake of simplicity

			#record latency for all sent pkts
			latency[nextpkt_dest] += ltcy


			if b.isEmpty():  # At this moment in some round, no remaining pkt pkts in buffer.
				break

			nextpkt = schedule(b, arg)
			nextpkt_dest = nextpkt.getToWhom()






	#record some results for each UE-------------------------
	for ue in b.getDrop_log():
		loss_bits[ue] = total_bits(b.getDrop_log()[ue])
		biterror_rate[ue] = loss_bits[ue] / gen.getLog()[ue]
		latency[ue] = latency[ue] / gen.getLog()[ue]

	print("----------------statistics----------------")
	print('@@scheduling method is ' +  '[' + algorithm + ']' + '\n')
	print("loss_bits", loss_bits, "\n")
	print("BER", biterror_rate, "\n")
	print("latancy per bit", latency, "\n")

	UEs_avgC = central_cell.UEs_avgC(simulation_time=simulation_T)
	print("UEs_avgC", UEs_avgC, "\n")



	scores = score(0, BER=biterror_rate, latency_per_bit=latency)
	print("score", scores)





	#make chart---------------------------------------------------
	#plz use list for making chart
	UE = []
	loss_bits_list = []
	biterror_rate_list = []
	latency_list = []

	for ue in range(N_UE):
		UE.append(ue)
		loss_bits_list.append(loss_bits[ue])
		biterror_rate_list.append(biterror_rate[ue])
		latency_list.append(latency[ue])






def main():
	Simulator("FIFO")





	Simulator("EDF")


	Simulator("SJF")

	Simulator("multi_queue")


	Simulator("RR")







if __name__ == '__main__':
    main()
