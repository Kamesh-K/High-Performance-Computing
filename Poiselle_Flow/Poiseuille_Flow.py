import math
import numpy as np 

del_y = 0.1
del_t = (del_y**2)/2
length = 2
mu = 0.0089
Dp_Dx = 0.005 
P = 4
size_list = int(length / del_y) + 1 
vel_arr = np.zeros((size_list))
diff_arr = np.zeros((size_list))
velocity = 0
nProcs = 1
size = nProcs
block_size = int(size_list / size)
local_vel_arr = np.empty(block_size).fill(0)
open('Velocity_Profile.txt', 'w').close()
vel_arr[size_list-1] = velocity
vel_arr_forward = np.concatenate([vel_arr[1:],vel_arr[:1]])
vel_arr_backward = np.concatenate([vel_arr[-1:],vel_arr[:-1]])
time_max = 4000
for time in range(time_max):
    diff_arr[:] = P*del_t + (del_t/(del_y**2))*(vel_arr_forward-2*vel_arr+vel_arr_backward)
    diff_arr[0] = 0
    diff_arr[size_list-1]=0
    vel_arr[:] = vel_arr[:] + diff_arr[:]
    vel_arr_forward = np.concatenate([vel_arr[1:],vel_arr[:1]])
    vel_arr_backward = np.concatenate([vel_arr[-1:],vel_arr[:-1]])
    print(vel_arr)
Y = np.linspace(-1,1,size_list)
Vel_analytical = 0.5*P*(1-Y**2)