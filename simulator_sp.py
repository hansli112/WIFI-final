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
N_UE = 12   #There are N_UE uniformly distributed in each cell
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

	simulation_T = 500
	loss_bits = {}   #record loss bits for each UE
	biterror_rate = {}
	latency = {}
    #record latency(total latency for all pkt) for each UE
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

	scores1 = score(0, BER=biterror_rate, latency_per_bit=latency)
	scores2 = score(0.5, BER=biterror_rate, latency_per_bit=latency)
	scores3 = score(1, BER=biterror_rate, latency_per_bit=latency)

	print(scores1)
	print(scores2)
	print(scores3)

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



	return biterror_rate_list, latency_list, UEs_avgC.tolist(), scores1, scores2, scores3







#satisfacation of UEs-------------------------------------------------
def score(factor, BER, latency_per_bit):
	#argument BER and latency_per_bit are dict

	metric = factor * np.array(list(BER.values()))+ (1 - factor) * np.array(list(latency_per_bit.values()))
	#output = 1 - np.true_divide(metric, sum(metric))
	temp_output = np.true_divide(metric, sum(metric))
	output = np.true_divide(1, temp_output)
	return output




def AlgorithmPerformance(UEs_score, numPriority=8): #This is just the score for any algorithm we used
	#type(UEs_score) is list
	miss = 0 		#perfect degree is equal to len(UEs_score) - 1
	P = {0: np.array([]), 1: np.array([]), 2: np.array([]), 3: np.array([]), 4: np.array([]), 5: np.array([]), 6: np.array([]), 7: np.array([])}

	total = 0  #total # of comparision

	degree = 0

	#group UEs' score based on priority
	for j in range(numPriority):
		for i in range(len(UEs_score)):
			if i % numPriority ==j:

				P[j] = np.append(P[j], UEs_score[i])

	#compare if all scores with higher priority is higher than all scores with lower priority
	for j in range(numPriority):
		for s in P[j]:

			if j == numPriority - 1:
				break   #prevend error from P[j+1] following


			miss += numFalse(s >= P[j+1])
			degree += sum(s - P[j+1])
			total += len(s >= P[j+1])

	Accuracy = np.true_divide((total - miss), total)
	Accuracy = np.multiply(Accuracy, 100)



	return (Accuracy, degree) #performance (%)



#used in AlgorithmPerformance function
def numFalse(narray):
	result = 0
	for f in narray:
		if f == False:
			result += 1

	return result






	return degree / (len(UEs_score) - 1) * 100




def main():
	'''
	Construct the 2 dim array for the bar plot
	w is width of array
	h is height of array
	'''
	w, h = N_UE, 6
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
	class_a[0], class_a[1], class_a[2], class_a[3], class_a[4], class_a[5] = Simulator("FIFO")


	class_b[0], class_b[1], class_b[2], class_b[3], class_b[4], class_b[5] = Simulator("EDF")
	class_c[0], class_c[1], class_c[2], class_c[3], class_c[4], class_c[5]  = Simulator("SJF")
	class_d[0], class_d[1], class_d[2], class_d[3], class_d[4], class_d[5]  = Simulator("multi_queue")
	class_e[0], class_e[1], class_e[2], class_e[3], class_e[4], class_e[5]  = Simulator("RR")

	'''
	This part is bits error rate
	'''
	#Plot bits error rate data-----------------------
	bar_width = 0.15
	xcor = np.arange(N_UE)
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
	x_name = []
	for i in range(N_UE):
		x_name.append('user'+str(i+1))

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
	plt.ylabel("Latency (s)")
	plt.ylim(0, 160)
	plt.title("Latency")

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
	This part is score for tradeoff factor = 0
	'''
	alpha = 0
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
	#plt.ylim(0, 160)
	plt.title("Scores (alpha=" + str(alpha) + ")")
	plt.legend()




	# Evaluation  the performance of the algorithms to the expected result.
	algorithms = ["FIFO", "RR", "EDF", "SJF", "MTQ"]
	y_pos = np.arange((len(algorithms)))

	algorithms_Accuracy = [AlgorithmPerformance(sc)[0] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]
	algorithms_performance = [AlgorithmPerformance(sc)[1] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]



	plt.figure(5)
	plt.bar(y_pos, algorithms_Accuracy, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("Acc (%)")
	plt.title("Accuracy(about Prioritizing UEs) of Algorithms (alpha=" + str(alpha) + ")")


	plt.figure(6)
	plt.bar(y_pos, algorithms_performance, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("performance")
	plt.title("Performance of Algorithms (alpha=" + str(alpha) + ")")





	'''
	This part is score for tradeoff factor = 0.5
	'''
	alpha = 0.5
	#Plot the scores data
	scor_a = class_a[4] * 100
	scor_b = class_b[4] * 100
	scor_c = class_c[4] * 100
	scor_d = class_d[4] * 100
	scor_e = class_e[4] * 100

	plt.figure(7)
	plt.bar(xcor, scor_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, scor_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, scor_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, scor_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, scor_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of Score plot
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Scores")
	#plt.ylim(0, 160)
	plt.title("Scores (alpha=" + str(alpha) + ")")
	plt.legend()




	# Evaluation  the performance of the algorithms to the expected result.
	algorithms = ["FIFO", "RR", "EDF", "SJF", "MTQ"]
	y_pos = np.arange((len(algorithms)))

	algorithms_Accuracy = [AlgorithmPerformance(sc)[0] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]
	algorithms_performance = [AlgorithmPerformance(sc)[1] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]



	plt.figure(8)
	plt.bar(y_pos, algorithms_Accuracy, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("Acc (%)")
	plt.title("Accuracy(about Prioritizing UEs) of Algorithms (alpha=" + str(alpha) + ")")


	plt.figure(9)
	plt.bar(y_pos, algorithms_performance, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("performance")
	plt.title("Performance of Algorithms (alpha=" + str(alpha) + ")")





	'''
	This part is score for tradeoff factor = 1
	'''
	alpha = 1
	#Plot the scores data
	scor_a = class_a[5] * 100
	scor_b = class_b[5] * 100
	scor_c = class_c[5] * 100
	scor_d = class_d[5] * 100
	scor_e = class_e[5] * 100

	plt.figure(10)
	plt.bar(xcor, scor_a, label = 'FIFO', width=bar_width, color = "green")
	plt.bar(xcor + bar_width, scor_b, label = 'RR', width=bar_width, color = "blue")
	plt.bar(xcor + 2*bar_width, scor_c, label = 'EDF', width=bar_width, color = "red")
	plt.bar(xcor + 3*bar_width, scor_d, label = 'SJF', width=bar_width, color = "yellow")
	plt.bar(xcor + 4*bar_width, scor_e, label = 'MTQ', width=bar_width, color = "black")

	#Label of Score plot
	plt.xticks(xcor + bar_width*2, x_name)
	plt.xlabel("users")
	plt.ylabel("Scores")
	#plt.ylim(0, 160)
	plt.title("Scores (alpha=" + str(alpha) + ")")
	plt.legend()




	# Evaluation  the performance of the algorithms to the expected result.
	algorithms = ["FIFO", "RR", "EDF", "SJF", "MTQ"]
	y_pos = np.arange((len(algorithms)))

	algorithms_Accuracy = [AlgorithmPerformance(sc)[0] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]
	algorithms_performance = [AlgorithmPerformance(sc)[1] for sc in [scor_a, scor_b, scor_c, scor_d, scor_e]]



	plt.figure(11)
	plt.bar(y_pos, algorithms_Accuracy, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("Acc (%)")
	plt.title("Accuracy(about Prioritizing UEs) of Algorithms (alpha=" + str(alpha) + ")")


	plt.figure(12)
	plt.bar(y_pos, algorithms_performance, align='center', alpha=0.5)
	plt.xticks(y_pos, algorithms)
	plt.ylabel("performance")
	plt.title("Performance of Algorithms (alpha=" + str(alpha) + ")")
	plt.show()








if __name__ == '__main__':
    main()
