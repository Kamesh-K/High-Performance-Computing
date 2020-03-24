# Program to solve the 1-D transient heat equation
# Importing the required libraries
import math
import random
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size
# Declaring the conditions of the system
del_x = 0.01
del_t = 0.01
length = 1
time_max = 100
alpha = 1.11 * 10**(-4)
size_list = int(length / del_x)
temp_arr = None
block_size = int(size_list / size)
local_temp_arr = np.empty(block_size).fill(0)
# Initializing the temperature array for 1-D
if rank == 0:
    temp_arr = np.empty([size, block_size], dtype='f')
    temp_arr.T[:, :] = 300
    temp_arr[size - 1, block_size - 1] = 500
local_temp_arr = np.empty(block_size, dtype='f')
# Scattering the array to different processes to do computations in those
# processes
comm.Scatter(temp_arr, local_temp_arr, root=0)
temp_1 = local_temp_arr
temp_2 = local_temp_arr
# Declaring and computing the constants for calculations
r = alpha * del_t / (del_x**2)
max_time_step = int(time_max / del_t)
time_step = 0
# Declaring elements which are received from other processes for computing
# the temperature evolution
left_elem = None
right_elem = None
# Declaring the file to dump the temperature evolution
open('Temperature_Profile.txt', 'w').close()
# Running the time loop for maximum limit set by the user
while time_step < max_time_step:
    # All the itermediate values in a sub domain is calculated for which no
    # data is required to be exchanged from the nearby processes
    for i in range(1, block_size - 1):
        temp_2[i] = temp_1[i] + r * \
            (temp_1[i + 1] - 2 * temp_1[i] + temp_1[i - 1])
    # For rank = 0, we need to receive only one data from rank = 1 for the
    # final element in rank 0
    if rank == 0:
        comm.send(temp_1[block_size - 1], dest=rank + 1, tag=time_step)
        right_elem = comm.recv(source=rank + 1, tag=time_step)
        temp_2[block_size - 1] = temp_1[block_size - 1] + r * \
            (right_elem - 2 * temp_1[block_size - 1] + temp_1[block_size - 2])
    # For rank = size - 1, we need to receive only one data from rank = size -
    # 2 for the final element in rank size - 1
    elif rank == size - 1:
        comm.send(temp_1[0], dest=rank - 1, tag=time_step)
        left_elem = comm.recv(source=rank - 1, tag=time_step)
        temp_2[0] = temp_1[0] + r * (temp_1[1] - 2 * temp_1[0] + left_elem)
    # For all intermediate ranks between rank 0 and rank size-1, we will have to receive two elements
    # One from the rank-1 process and one from rank+1 process
    # Suitable equations are written so that this is take care of
    else:
        comm.send(temp_1[block_size - 1], dest=rank + 1, tag=time_step)
        comm.send(temp_1[0], dest=rank - 1, tag=time_step)
        left_elem = comm.recv(source=rank - 1, tag=time_step)
        right_elem = comm.recv(source=rank + 1, tag=time_step)
        temp_2[block_size - 1] = temp_1[block_size - 1] + r * \
            (right_elem - 2 * temp_1[block_size - 1] + temp_1[block_size - 2])
        temp_2[0] = temp_1[0] + r * (temp_1[1] - 2 * temp_1[0] + left_elem)
    temp_1 = temp_2
    time_step += 1  # Incrementing the time iter and looping continues
    # Gather all the computed temperature profile and place it in temp_arr
    comm.Gather(temp_1, temp_arr, root=0)

    if rank == 0:
        # Dump the temp_arr in the file and keep appending till the loop runs
        temp_csv = np.reshape(temp_arr, (1, size_list))
        with open("Temperature_Profile.txt", "a") as myfile:
            np.savetxt(myfile, temp_csv, fmt='%1.4e', delimiter=",")
