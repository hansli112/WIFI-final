import matplotlib.pyplot as plt
from matplotlib import path
import numpy as np
from schedule import *
from channel import *

class Cell:
	#1.generate hexagon 2.scatter UEs

	def __init__(self, BS_pos, BS_buffer, radius, ID=0):
		#declare a cell
		self.BS_pos = BS_pos
		self.BS_buffer = BS_buffer
		self.radius = radius
		self.ID = ID


	def gen_cell(self):
		#Really generate cell
		'''

		:return:(np array)with shape (2,7) which 7 is the number of vertex plus 1
		'''
		#generate a hexagon
		L = np.linspace(0, 2*np.pi, 7)
		xv = self.BS_pos[0] + self.radius * np.cos(L)
		yv = self.BS_pos[1] + self.radius * np.sin(L)

		return np.array([xv, yv])

	def gen_UEs(self, xv, yv, N_UE):
		#generate UEs
		'''

		:param xv, yv: position of central_BS
		:param N_UE: # of UEs
		:return: (np array)with shape (N_UE,2)
		'''
		#generate random distributed UEs within the cell
		counter = 1
		self.N_UE = N_UE
		self.UEs_pos = []

		tmp = np.transpose(np.array([xv, yv]))

		cell_coverage = path.Path(tmp)


		while counter <= N_UE:
			UE_x = np.random.uniform(-1, 1, 1) * self.radius + self.BS_pos[0]
			UE_y = np.random.uniform(-1, 1, 1) * self.radius + self.BS_pos[1]
			pos = np.concatenate((UE_x, UE_y), axis=None)


			if cell_coverage.contains_points([pos]):
				self.UEs_pos.append(pos)

				counter += 1

		self.UEs_pos = 	np.array(self.UEs_pos)

		return self.UEs_pos



	def UEs_throughput(self, AllCells_pos, cell_bandwidth=10 * 10 ** 6):
			'''AllCells_pos is a numpy array of all position of cell in topology'''


			#parameter setting
			#temporarily hard code
			Tx_h=1.5 + 50
			Rx_h=1.5
			Tx_gain = 14
			Rx_gain = 14
			Tx_power = 33 - 30  #convert to dB
			temperature = 27 + 273.15  # degree Kelvin
			thermal_noise_p = (1.38 * 10 ** (-23)) * temperature * 10 * (10 ** 6)



			UE_bandwidth = (cell_bandwidth) / 50  #Hz
			#print(UEs_pos)
			#print("-------")
			dist2central_BS = [0 , 0] - self.UEs_pos

			dist2central_BS = (dist2central_BS[:,0]**2 + dist2central_BS[:,1]**2)**0.5

			#calculate rx power on each UE
			PL = loss_model(dist2central_BS, Tx_h, Rx_h) #include fading effect
			rx_power = rx_Power(PL,Tx_power, Tx_gain, Rx_gain)

			#print('-------------------------------------')

			#calculate interference for each UE(summation all power rx from other BS when considering 1 UE)


			interference_p = np.zeros((self.N_UE,), dtype=float) #collect total interference for each UE from other BS except for central_BS
			#print(interference_p)
			for bs in np.delete(AllCells_pos, self.BS_pos):
					dist = bs - self.UEs_pos  # distance between specified BS and each UE
					dist = (dist[:,0]**2 + dist[:,1]**2)**0.5
					PL1 = two_ray_model(dist, Tx_h, Rx_h)
					interference = 10**(rx_Power(PL1,Tx_power, Tx_gain, Rx_gain) / 10)  #interference add in Watt


					interference_p += interference

			#print("interference_p", interference_p)
			UEs_SINR = SINR(rx_power, interference_p, thermal_noise_p) #in dB
			#print("UEs_SINR",UEs_SINR)

			UEs_SINR = 10**(UEs_SINR/10)
			#print('2', UEs_SINR)
			C = shannon_capacity(UE_bandwidth, UEs_SINR) #ideal throughput for all UE

			return C  #type(C) is numpy array


	def GetBuffer(self):
		return self.BS_buffer


class UE:
	def __init__(self, position, rxBit, ID, priority):
		self.position = position
		self.priority = priority
		self.rxBit = rxBit
		self.ID = ID



def main():
	'''
	a = Topology(50, [0, 0])
	a.plot()
	print(a.getUE().shape)


	a = Cell([600,600])
	b = Cell([0, 0])
	a.plot()
	b.plot()
	plt.show()

	x = CellMap([0,0])
	x.plot()
	y = CellMap([4.5*500/(3**0.5), 1750])
	y.plot()
	plt.show()
	'''
	a = Cell([0,0], 50)
	z = a.gen_cell()
	print("z[0]", z[0])

	print("z[1]", z[1])
	plt.figure()

	plt.plot(z[0], z[1])

	UE = a.gen_UEs(z[0], z[1], 10)
	print(UE.shape)

	plt.plot(UE[:,0], UE[:,1], "ro")
	plt.show()


if __name__ == '__main__':
		main()
