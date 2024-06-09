def by_size(mat,thresh):
	maxv = np.amax(mat)
	locs = [[] for i in xrange(int(maxv))]
	dim1,dim2 = np.shape(mat)
	for i in xrange(dim1):
		for j in xrange(dim2):
			if int(mat[i][j]) != 0:
				locs[int(mat[i][j]-1)].append([i,j])
	centroids = []
	for i in xrange(len(locs)):
		if len(locs[i])>thresh:
			xs,ys = np.transpose(np.array(locs[i]))
			dx = np.amax(xs) - np.amin(xs)
			dy = np.amax(ys) - np.amin(ys)

			if dx > 400 and dy > 400:
				a = range(len(xs))
				a = np.random.permutation(a)
				for j in xrange(5000):
					centroids.append([ys[a[j]],xs[a[j]]])
			else:
				r = np.random.permutation(range(len(xs)))[0]
				cx = np.mean(xs)
				cy = np.mean(ys)
				
				centroids.append([cy,cx]) 
	xt = np.transpose(centroids)[0]
	yt = np.transpose(centroids)[1]
	return np.array(centroids)