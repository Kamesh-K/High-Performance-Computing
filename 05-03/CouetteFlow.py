# Program to solve a 2-D couette flow of fluid 
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size
# Declaring the array and setting the seed for random
del_y = 0.1
del_t = 1 
length = 10
time_max = 10000
mu = 0.0089
rho = 1000
r = (mu * del_t/(rho * del_y**2))
size_list = int(length/del_y) 
vel_arr = None
velocity = 5.0
block_size = int(size_list/size)
local_vel_arr = np.empty(block_size).fill(0)
open('Velocity_Profile.txt', 'w').close()	
sendbuf = None
if rank == 0:
    vel_arr = np.empty([size, block_size], dtype='f')
    vel_arr.T[:,:] = 0
    vel_arr[size-1,block_size-1] = velocity
local_vel_arr = np.empty(block_size, dtype='f')
comm.Scatter(vel_arr, local_vel_arr, root=0)
u_1 = local_vel_arr
u_2 = local_vel_arr
max_time_step = int(time_max/del_t)
time_step = 0 
left_elem = None 
right_elem = None 
while time_step < max_time_step:
	for i in range(1,block_size-1):
		u_2[i]= u_1[i] + r*(u_1[i+1] - 2*u_1[i] + u_1[i-1])
	if rank == 0:
		comm.send(u_1[block_size-1], dest = rank+1, tag = time_step)
		right_elem = comm.recv(source = rank+1,tag = time_step)
		u_2[block_size-1] = u_1[block_size-1] + r*(right_elem - 2*u_1[block_size-1]+ u_1[block_size-2])
	elif rank == size - 1:
		comm.send(u_1[0],dest = rank-1, tag = time_step)
		left_elem = comm.recv(source = rank -1, tag = time_step)
		u_2[0] = u_1[0] + r*(u_1[1] - 2*u_1[0] + left_elem)
	else:
		comm.send(u_1[block_size-1], dest = rank+1, tag = time_step)
		comm.send(u_1[0],dest = rank-1, tag = time_step)
		left_elem = comm.recv(source = rank -1, tag = time_step)
		right_elem = comm.recv(source = rank+1,tag = time_step)
		u_2[block_size-1] = u_1[block_size-1] + r*(right_elem - 2*u_1[block_size-1]+ u_1[block_size-2])
		u_2[0] = u_1[0] + r*(u_1[1] - 2*u_1[0] + left_elem)
	u_1 = u_2 
	time_step += 1
	comm.Gather(u_1,vel_arr,root =0)

	if rank ==0:
		vel_csv = np.reshape(vel_arr,(1,size_list))
		with open("Velocity_Profile.txt", "a") as myfile:
		 	np.savetxt(myfile, vel_csv, fmt='%1.4e', delimiter=",")
