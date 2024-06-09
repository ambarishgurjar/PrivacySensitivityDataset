

from PIL import Image
from numpy import array
import pandas as pd
import numpy as np
import PIL
import matplotlib
import matplotlib.pyplot as plt


def gradient_train(p_delta_f,LOSS_instance,filter):
  no_of_itrs =  2250
  loss_function = []
  
  while (no_of_itrs):

    filter = filter + p_delta_f
#    print(filter)
    (new_p_delta_f,LOSS_instance,filter) = loss_updater(filter)
    LOSS_instance = LOSS_instance[-1]
    a = LOSS_instance[0]
    loss_function.append(a)

#    gradient_train(new_p_delta_f,new_LOSS_instance,filter)  
    no_of_itrs = no_of_itrs - 1
    
 
  return(loss_function)
     
def loss_updater(f_vector):
  
  F_t_X = np.matmul(np.transpose(f_vector),X_PATCHES)
  G_of_f_t_X = 1 / (1 + (np.exp(-F_t_X)))
  S_t_minus_G = np.subtract(S_t, G_of_f_t_X)
#  plt.imshow (S_t_minus_G.reshape(no_of_patches_oneway,no_of_patches_oneway),cmap='gray')
  G_prime_F_t_X = (G_of_f_t_X * (1 - G_of_f_t_X))

  dot_product = S_t_minus_G * G_prime_F_t_X
# plt.imshow (dot_product.reshape(no_of_patches_oneway,no_of_patches_oneway),cmap='gray')
  N = no_of_patches_oneway * no_of_patches_oneway

  de_df = -2/N * np.matmul(X_PATCHES,np.transpose(dot_product))
  delta_f = - de_df

  p_delta_f = p * delta_f
  LOSS_instance = 1/N * np.dot((S_t_minus_G),np.transpose(S_t_minus_G))

  return(p_delta_f,LOSS_instance,f_vector)

