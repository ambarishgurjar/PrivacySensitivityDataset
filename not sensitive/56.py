def grow_mask(start_positionx, start_positiony):

	a,b = np.shape(tmp)
	checked = {}
	to_check = []
	to_check.append([start_positionx, start_positiony])
	while len(to_check) != 0:
		next_to_checkx, next_to_checky = to_check.pop(0)
		if not (checked.get(tuple([next_to_checkx, next_to_checky]), None)) and (tmp[next_to_checkx, next_to_checky] == 0):
			if next_to_checkx+1 < a:
				to_check.append([next_to_checkx+1, next_to_checky])
			if next_to_checky+1 < b:
				to_check.append([next_to_checkx, next_to_checky+1])
			if next_to_checkx-1 >= 0:
				to_check.append([next_to_checkx-1, next_to_checky])
			if next_to_checky-1 >= 0:
				to_check.append([next_to_checkx, next_to_checky-1])
			checked[tuple([next_to_checkx, next_to_checky])] = True
			tmp2[next_to_checkx, next_to_checky] = 0
			print "length of to check:", len(to_check)
			print "length of checked:", len(checked)
	return tmp2

def refine_mask(data, mask):

	mask2 = np.copy(mask)
	xs,ys = np.where(mask == 0)
	print 'STARTED WITH '+str(len(xs))
	tocheck = []
	for i in xrange(len(xs)):
		tocheck.append(data[xs[i]][ys[i]])
	tocheck = np.unique(tocheck)
	print 'to check is: \n'
	print 'tocheck ids:', tocheck
	dim1 , dim2 = np.shape(data)
	for i in xrange(dim1):
		for j in xrange(dim2):
			if data[i][j] in tocheck:
				mask2[i][j] = 0
	xs,ys = np.where(mask2 == 0)
	print 'ENDED WITH '+str(len(xs))
	return mask2