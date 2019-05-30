import numpy as np
from matplotlib import pyplot as plt


#path loss gain model(in dB)
def two_ray_model(d, h_t, h_r):

	return 10 * np.log10(((h_t*h_r) ** 2) / d ** 4)



def loss_model(d, h_t, h_r):
	'''
	All unit are dB!!
	'''
	pathloss = two_ray_model(d, h_t, h_r)
	fading = np.random.normal(0, 6) #np.random.normal(mean, sigma)

	return pathloss + fading





def SINR(rx_power, interference_noise_p, thermal_noise_p):
	'''

	:param rx_power in (dB)
		   interference_noise_p, thermal_noise_p (Watt)

	:return: SINR in dB
	'''
	# 10 ** (rx_power / 10)把rx power換成Watt
	SINR = 10 * np.log10(10 ** (rx_power / 10) / (interference_noise_p + thermal_noise_p))
	return SINR




def ith_SINR(All_rx_power, index, thermal_noise_p):
	#divide All_rx_power into rx_power and interference
	'''
	:param thermal_noise_p: (Watt)
	:param total_rx_power: (numpy array N*1) N is the number of measured power (dB)
	:param index:  index of deisired rx_power except for interference
	:return:
	'''
	interference_noise_p = (10 ** (All_rx_power/10)).sum() - 10 ** (All_rx_power[index]/10) #(Watt)
	ith_SINR = SINR(All_rx_power[index], interference_noise_p, thermal_noise_p)

	return ith_SINR



def rx_Power(PL,tx_power, tx_gain, rx_gain):
	'''
		[all unit are dB!!!]
	'''
	rx_power = PL + tx_power + tx_gain + rx_gain
	return rx_power

def main():
	tx_p = 33 - 30 #dB
	tx_gain = 14
	rx_gain = 14
	h_t = 1.5 + 50
	h_r = 1.5
	d = np.linspace(1, 1000)

	#plot 1-1


	rx_power = two_ray_model(d, h_t, h_r) + tx_p + tx_gain + rx_gain  #(dB)
	plt.figure()

	plt.title('rx power(only pathloss) vs. distance in two-ray-ground model')

	plt.xlabel('distance(m)')
	plt.ylabel('receive power(dB)')

	plt.plot(d, rx_power, color='red')
	#plt.show()


	# plot 1-2

	temperature = 27 + 273.15   # degree Kelvin
	thermal_noise_p = (1.38 * 10 ** (-23)) * temperature * 10 * (10 ** 6)
	interference_noise_p = 0 (Watt)

	SINR = 10 * np.log10(10 ** (rx_power / 10) / (interference_noise_p + thermal_noise_p))

	plt.figure()


	plt.title('SINR(without interference) vs. distance in two-ray-ground model')
	plt.xlabel('distance(m)')
	plt.ylabel('SINR(dB)')
	plt.plot(d, SINR, color='green', linewidth=2.5)
	#plt.show()


	# plot 2-1
	normal_distribution = np.random.normal(0, 6, rx_power.size)
	rx_power += normal_distribution

	plt.figure()

	plt.title('rx power(with shadowing) vs. distance in two-ray-ground model')
	plt.xlabel('distance(m)')
	plt.ylabel('receive power(dB)')
	plt.plot(d, rx_power, color='blue', linewidth=2.5)
	#plt.show()


	# plot 2-2

	SINR = 10 * np.log10(10 ** (rx_power / 10) / (interference_noise_p + thermal_noise_p))
	plt.figure()

	plt.title('SINR(wothout interference) vs. distance in two-ray-ground model')

	plt.xlabel('distance(m)')
	plt.ylabel('SINR(dB)')

	plt.plot(d, SINR, color='gray', linewidth=2.5)
	plt.show()


if __name__ == '__main__':
	main()
