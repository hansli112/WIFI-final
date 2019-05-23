import matplotlib.pyplot as plt
from matplotlib import path
import numpy as np


class Cell:
	#1.generate hexagon 2.scatter UEs

	def __init__(self, BS_pos, radius, ID=0):
		#declare a cell
		self.BS_pos = BS_pos
		self.radius = radius
		self.ID = ID

	def gen_cell(self):
		'''

		:return:(np array)with shape (2,7) which 7 is the number of vertex plus 1
		'''
		#generate a hexagon
		L = np.linspace(0, 2*np.pi, 7)
		xv = self.BS_pos[0] + self.radius * np.cos(L)
		yv = self.BS_pos[1] + self.radius * np.sin(L)

		return np.array([xv, yv])

	def gen_UEs(self, xv, yv, N_UE):
		'''

		:param xv:
		:param yv:
		:param N_UE:
		:return: (np array)with shape (N_UE,2)
		'''
		#generate random distributed UEs within the cell
		counter = 1
		UE_pos = []

		tmp = np.transpose(np.array([xv, yv]))

		cell_coverage = path.Path(tmp)


		while counter <= N_UE:
			UE_x = np.random.uniform(-1, 1, 1) * self.radius + self.BS_pos[0]
			UE_y = np.random.uniform(-1, 1, 1) * self.radius + self.BS_pos[1]
			pos = np.concatenate((UE_x, UE_y), axis=None)


			if cell_coverage.contains_points([pos]):
				UE_pos.append(pos)

				counter += 1

		return np.array(UE_pos)



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
