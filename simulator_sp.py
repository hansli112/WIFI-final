from cell import *
import matplotlib.pyplot as plt
from matplotlib import path
import numpy as np
from traffic import *
from channel import *
from schedule import *
import matplotlib.pyplot as plt

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
'''
plt.figure()
plt.title("1-1 Topology")
plt.xlabel('x axis(m)')
plt.ylabel('y axis(m)')

plt.plot(tmp[0], tmp[1])   #plot cell

plt.plot(0, 0, 'r^')
'''
# create UEs and at the same time create buffers for each UE-------------
UEs_pos = central_cell.gen_UEs(tmp[0], tmp[1], N_UE)
'''
plt.plot(UEs_pos[:, 0], UEs_pos[:, 1], "b*")

plt.show()
'''




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
		biterror_rate[ue] = np.true_divide(loss_bits[ue], gen.getLog()[ue])
		latency[ue] = np.true_divide(latency[ue], gen.getLog()[ue])

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

	

	return biterror_rate_list, latency_list, UEs_avgC.tolist(), scores



def score(factor, BER, latency_per_bit):
	#argument BER and latency_per_bit are dict

	metric = factor * np.array(list(BER.values()))+ (1 - factor) * np.array(list(latency_per_bit.values()))
	output = 1 - np.true_divide(metric, sum(metric))
	return output



def main():
	'''
	Construct the 2 dim array for the bar plot
	w is width of array 
	h is height of array
	'''
	w, h = 10, 4
	class_a = [[0 for i in range(w)] for j in range(h)]
	class_b = [[0 for i in range(w)] for j in range(h)]
	class_c = [[0 for i in range(w)] for j in range(h)]
	class_d = [[0 for i in range(w)] for j in range(h)]
	class_e = [[0 for i in range(w)] for j in range(h)]

	'''
	index 0 is bits error rate
	index 1 is latency
	index 2 is UE's average receive capacity
	index 3 is scores
	'''
	class_a[0], class_a[1], class_a[2], class_a[3] = Simulator("FIFO")
	class_b[0], class_b[1], class_b[2], class_b[3] = Simulator("EDF")
	class_c[0], class_c[1], class_c[2], class_c[3] = Simulator("SJF")
	class_d[0], class_d[1], class_d[2], class_d[3] = Simulator("multi_queue")
	class_e[0], class_e[1], class_e[2], class_e[3] = Simulator("RR")

	'''
	This part is bits error rate
	'''
	#Plot bits error rate data
	bar_width = 0.15
	xcor = np.arange(10)
	ber_a = np.multiply(class_a[0], 100)
	ber_b = np.multiply(class_b[0], 100)
	ber_c = np.multiply(class_c[0], 100)
	ber_d = np.multiply(class_d[0], 100)
	ber_e = np.multiply(class_e[0], 100)

	plt.figure(1)
	plt.bar(xcor, ber_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, ber_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, ber_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, ber_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, ber_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of capacity plot
	x_name =  ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Bits error rate")
	plt.ylim(0, 160)
	plt.title("BER")

	#Plot legend and the plot
	plt.legend()

	'''
	This part is latency part
	'''
	#Plot capacity data
	late_a = np.multiply(class_a[1], 1000)
	late_b = np.multiply(class_b[1], 1000)
	late_c = np.multiply(class_c[1], 1000)
	late_d = np.multiply(class_d[1], 1000)
	late_e = np.multiply(class_e[1], 1000)

	plt.figure(2)
	plt.bar(xcor, late_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, late_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, late_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, late_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, late_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of capacity plot
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Capacity (bits/s)")
	plt.ylim(0, 160)
	plt.title("Capacity")

	#Plot legend and the plot
	plt.legend()


	'''
	This part is capacity part
	'''
	#Plot capacity data
	cap_a = np.true_divide(class_a[2], 1000)
	cap_b = np.true_divide(class_b[2], 1000)
	cap_c = np.true_divide(class_c[2], 1000)
	cap_d = np.true_divide(class_d[2], 1000)
	cap_e = np.true_divide(class_e[2], 1000)
	
	plt.figure(3)
	plt.bar(xcor, cap_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, cap_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, cap_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, cap_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, cap_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of capacity plot
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Capacity (bits/s)")
	plt.ylim(0, 160)
	plt.title("Capacity")

	#Plot legend and the plot
	plt.legend()


	'''
	This part is score
	'''
	#Plot the scores data
	scor_a = class_a[3] * 100
	scor_b = class_b[3] * 100
	scor_c = class_c[3] * 100
	scor_d = class_d[3] * 100
	scor_e = class_e[3] * 100

	plt.figure(4)
	plt.bar(xcor, scor_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, scor_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, scor_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, scor_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, scor_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of Score plot
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Scores")
	plt.ylim(0, 160)
	plt.title("Scores")
	plt.legend()

	plt.show()




if __name__ == '__main__':
    main()
