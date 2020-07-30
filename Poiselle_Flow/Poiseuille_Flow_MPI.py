# Program to solve for a poiseuille flow in a pipe 
# Importing the required libraries
import math
import random
import numpy as np
import time
from mpi4py import MPI
import seaborn as sns
import matplotlib.pyplot as plt 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
size = nProcs
np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)
start_time = time.time()
del_y = 0.1
del_t = (del_y**2)/2
length = 2
P = 4
size_list = int(length / del_y) 
vel = None
vel_aux = None 
error = 100 
tolerance = 10**-3
if rank==0:
    vel= np.zeros((size_list))
    vel_aux = np.zeros((size_list))
block_size = int(size_list / size)
local_diff = np.zeros(block_size)
local_vel= np.zeros(block_size)
comm.Scatter(vel,local_vel,root=0)
time_max = 10000
left_elem = None 
right_elem = None 
time_step = 0 
while time_step < time_max and error > tolerance:
    time_step = time_step + 1 
    if rank == 0:
        comm.send(local_vel[block_size - 1], dest=rank + 1, tag=time_step)
        right_elem = comm.recv(source = rank+1,tag = time_step)
        vel_forward = np.hstack((local_vel[1:],right_elem))
        vel_backward = np.hstack((0.0,local_vel[:-1]))
        local_diff[:] = P*del_t + (del_t/(del_y**2))*(vel_forward-2*local_vel+vel_backward)
        local_diff[0] = 0
        local_vel[:] = local_vel[:] + local_diff[:]
    elif rank == size-1:
        comm.send(local_vel[0],dest = rank-1,tag=time_step)
        left_elem = comm.recv(source = rank-1, tag=time_step)
        vel_forward = np.hstack((local_vel[1:],0.0))
        vel_backward = np.hstack((left_elem,local_vel[:-1]))
        local_diff[:] = P*del_t + (del_t/(del_y**2))*(vel_forward-2*local_vel+vel_backward)
        local_vel[:] = local_vel[:] + local_diff[:]
    else:
        comm.send(local_vel[block_size - 1], dest=rank + 1, tag=time_step)
        comm.send(local_vel[0],dest = rank-1,tag=time_step)
        left_elem = comm.recv(source = rank-1, tag=time_step)
        right_elem = comm.recv(source = rank+1,tag = time_step)
        vel_forward = np.hstack((local_vel[1:],right_elem))
        vel_backward = np.hstack((left_elem,local_vel[:-1]))
        local_diff[:] = P*del_t + (del_t/(del_y**2))*(vel_forward-2*local_vel+vel_backward)
        local_vel[:] = local_vel[:] + local_diff[:]
    comm.Gather(local_vel,vel_aux,root=0)
    if rank==0:
        error = np.sum(np.abs(np.subtract(vel,vel_aux)))
        vel[:] = vel_aux[:]
        print("Timestep - {} and Error - {}".format(time_step,error))
    error = comm.bcast(error,root=0)
if rank == 0:
    print(vel)
    print("Total execution time - {}".format(time.time()-start_time))
    actual_vel = np.hstack((vel,0))
    x_domain = np.linspace(-length/2,length/2,size_list+1)
    plt.plot(actual_vel,x_domain,'r')
    surface = np.ones(size_list+1)*length/2  
    plt.plot(actual_vel,surface,'b')
    plt.plot(actual_vel,-surface,'b')
    plt.xlabel("Velocity along the axis")
    plt.ylabel("Distanc from the center of plates")
    plt.show()