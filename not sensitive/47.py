

import random
import statistics
Centroids = np.array(4)
Centroids = [1,10,20,30]

initial_centroid = np.zeros(4)

#print(Centroids)

Cen0collection = []
Cen1collection = []
Cen2collection=[]
Cen3collection =[]

disparity_copy  = disparity_matrix.reshape(-1)
cluster_no_holder = np.ones(disparity_copy.shape)
itr = 50
while(itr>0):
      #print(itr)
      for i in range(disparity_copy.shape[0]):
        Min_Diff = 40
        for k in range(0,4):
            Diff = abs(Centroids[k] - disparity_copy[i])
            if Diff < Min_Diff:
              Min_Diff = Diff
              #print(i,Diff,disparity_copy[i])
              cluster_no_holder[i] = k


      for i in range(disparity_copy.shape[0]):
        if cluster_no_holder[i] == 0:
          Cen0collection.append(disparity_copy[i])
        if cluster_no_holder[i] == 1:
          Cen1collection.append(disparity_copy[i])
        if cluster_no_holder[i] == 2:
          Cen2collection.append(disparity_copy[i])
        if cluster_no_holder[i] == 3:
          Cen3collection.append(disparity_copy[i])



      Centroids[0] = statistics.mean(Cen0collection)
      Centroids[1] = statistics.mean(Cen1collection)
      Centroids[2] = statistics.mean(Cen2collection)
      Centroids[3] = statistics.mean(Cen3collection)

      #print(Centroids[0],Centroids[1],Centroids[2],Centroids[3])

      if (Centroids[0] - initial_centroid[0]) + (Centroids[1] - initial_centroid[1]) + (Centroids[2] - initial_centroid[2]) == 0:
        break
      else:
        initial_centroid[0] = Centroids[0]
        initial_centroid[1] = Centroids[1]
        initial_centroid[2] = Centroids[2]
        initial_centroid[3] = Centroids[3]

      itr-=1
      
