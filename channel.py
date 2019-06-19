"""
This project calssify some function of communication model,
like two_way_ground model, SINR, shannon capacity.You can use
belows function for building model
"""
import numpy as np
from matplotlib import pyplot as plt
np.random.seed(0)


#watt transfer to dB
def watt2dB(power):
    return 10 * np.log10(power)

#dB transfer to watt
def dB2watt(power_dB):
    return 10**((power_dB)/10)

#transfer dBm to dB
def dBm2dB(power_dBm):
    return power_dBm - 30

#path loss gain model by two way ground model(in dB)
def two_ray_model(d, h_t, h_r):
    power = ((h_t*h_r) ** 2 ) / (d ** 4)
    return watt2dB(power)

#add fading to the two-way-ground model's pass loss
#pathloss ==> unit: dB
#fading   ==> add some value in pdf(normal distribution)
def loss_model(d, h_t, h_r):
	pathloss = two_ray_model(d, h_t, h_r)
	fading = np.random.normal(0, 6) #np.random.normal(mean, sigma)
	return pathloss + fading

#Calculate the SINR of UE
#rx_power : signals                     unit: dB
#interference_noise_p : interferences   unit: watt
#thermal_noise_p : noise		unit: watt
#SINR_dB : the SINR value               unit: dB
def SINR(rx_power, interference_noise_p, thermal_noise_p):
    SINR_watt = dB2watt(rx_power) / (interference_noise_p + thermal_noise_p)
    SINR_dB = watt2dB(SINR_watt)
    return SINR_dB

#Calculate the SINR by considering the other base stations' interference
#All_rx_power : signals from all base stations  unit:dB
#index : which UE
#thermal_noise_p : noise                        unit: watt
def ith_SINR(All_rx_power, index, thermal_noise_p):
    interference_noise_p = dB2watt(All_rx_power).sum() - dB2watt(All_rx_power[index])
    ith_SINR = SINR(All_rx_power[index], interference_noise_p, thermal_noise_p)
    return ith_SINR

#Calculate the capacity between UE and BS by shannon capacity
#bandwidth     unit: Hz
#SINR          unit: dB
#capacity      unit: bits/s
def shannon_capacity(bandwidth, SINR):
    capacity = bandwidth * np.log2(1 + SINR)
    return capacity

#Calculate the receive power
#PL : path loss
#tx_power : transmitter's power   unit: dB
#tx_gain  : transmitted gain	  unit: dB
#rx_gain  : received gain	  unit: dB
#rx_power : received power	  unit: dB
def rx_Power(PL,tx_power, tx_gain, rx_gain):
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
	interference_noise_p = 0 #Watt

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
