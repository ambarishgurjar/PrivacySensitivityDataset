
import numpy as np



def encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf):



	filterbank = gaborconvolve(polar_array, minWaveLength, mult, sigmaOnf)

	length = polar_array.shape[1]
	template = np.zeros([polar_array.shape[0], 2 * length])
	h = np.arange(polar_array.shape[0])


	mask = np.zeros(template.shape)
	eleFilt = filterbank[:, :]


	H1 = np.real(eleFilt) > 0
	H2 = np.imag(eleFilt) > 0


	H3 = np.abs(eleFilt) < 0.0001
	for i in range(length):
		ja = 2 * i

		template[:, ja] = H1[:, i]
		template[:, ja + 1] = H2[:, i]


		mask[:, ja] = noise_array[:, i] | H3[:, i]
		mask[:, ja + 1] = noise_array[:, i] | H3[:, i]

	return template, mask



def gaborconvolve(im, minWaveLength, mult, sigmaOnf):

	rows, ndata = im.shape			