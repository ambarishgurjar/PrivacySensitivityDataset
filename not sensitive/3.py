def segmentation3(filename,cx,cy,dx,dy,times):

	iterator = 0 
	file_counter = 0
	x = np.arange(0, dy)
	y = np.arange(0, dx)
	X, Y = np.meshgrid(x, y)
	tmp = np.zeros((dx,dy))
	print 'Initilializing'
	shuffler = range(len(cx))
	shuffler = np.random.permutation(shuffler)
	for i in xrange(len(cx)):
		tmp[cy[i]][cx[i]] = shuffler[i]+1
	todo = []
	for i in xrange(len(cx)):
		todo.append(expand(int(cy[i]),int(cx[i]),tmp,dx,dy))
	print 'made to do'
	tmin= np.amin(times)
	tmax= np.amax(times)
	t = 0
	dt = 0.025*10

	speed_up = True
	if speed_up == True:
		upper_t = (tmax + 1) + 5
	else:
		upper_t = tmax+1
	while t< upper_t:
		if speed_up == True:
			if t > 200: 
				dt = dt * 1.0005
		tmp2 = np.copy(tmp)
		lens = [ len(list(set(todo[i]))) for i in xrange(len(todo))]
		tmp_list = [[] for i in xrange(len(cx))]
		shuffler_for_order = range(len(cx))
		shuffler_for_order = np.random.permutation(shuffler_for_order)
		for ii in range(len(cx)):
			i = shuffler_for_order[ii]
			list_to_do = list(set(todo[i]))
			if list_to_do != []:
				for j in xrange(len(list_to_do)):
					if times[list_to_do[j][0],list_to_do[j][1]] < t and tmp[list_to_do[j][0],list_to_do[j][1]]==0:
						tmp[list_to_do[j][0],list_to_do[j][1]] = shuffler[i]+1
						addon = expand(list_to_do[j][0],list_to_do[j][1],tmp2,dx,dy)
						if addon != []:
							for k in range(len(addon)):
								tmp_list[i].append(addon[k])
					elif times[list_to_do[j][0],list_to_do[j][1]] > t:
						tmp[list_to_do[j][0],list_to_do[j][1]] = 0
						tmp_list[i].append(list_to_do[j])
		todo = tmp_list[:]
		iterator += 1
		t+=dt
		print m,t,tmax

		save_int = True
		save_freq = 100
		if save_int:
			if iterator%save_freq == 0:
				np.savetxt('./'+filename+'_FMM_seg.csv',tmp.astype(int), fmt='%i',delimiter=',')
	np.savetxt('./'+filename+'_FMM_seg.csv',tmp.astype(int), fmt='%i',delimiter=',')