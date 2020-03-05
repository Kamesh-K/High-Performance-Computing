# Program to sort a solve the 1-D transient heat equation  
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
del_x = 0.01
del_t = 0.01 
length = 1
time_max = 100
alpha = 1.11 * 10**(-4)
size_list = int(length/del_x) 
temp_arr = None
block_size = int(size_list/size)
local_temp_arr = np.empty(block_size).fill(0)
#temp_arr = [300]*size_list;
sendbuf = None
if rank == 0:
    temp_arr = np.empty([size, block_size], dtype='f')
    temp_arr.T[:,:] = 300
    temp_arr[size-1,block_size-1]=500
local_temp_arr = np.empty(block_size, dtype='f')
comm.Scatter(temp_arr, local_temp_arr, root=0)
temp_1 = local_temp_arr
temp_2 = local_temp_arr
r = alpha * del_t/(del_x**2)
max_time_step = int(time_max/del_t)
time_step = 0 
left_elem = None 
right_elem = None 
open('Temperature_Profile.txt', 'w').close()	
#if rank ==0:
#	index_table = np.arange(1,size_list)
#	with open("Temperature_Profile.txt", "a") as myfile:
#	 	np.savetxt(myfile, index_table, fmt='%1.4e')

while time_step < max_time_step:
	for i in range(1,block_size-1):
		temp_2[i]= temp_1[i] + r*(temp_1[i+1] - 2*temp_1[i] + temp_1[i-1])
	if rank == 0:
		comm.send(temp_1[block_size-1], dest = rank+1, tag = time_step)
		right_elem = comm.recv(source = rank+1,tag = time_step)
		temp_2[block_size-1] = temp_1[block_size-1] + r*(right_elem - 2*temp_1[block_size-1]+ temp_1[block_size-2])
	elif rank == size - 1:
		comm.send(temp_1[0],dest = rank-1, tag = time_step)
		left_elem = comm.recv(source = rank -1, tag = time_step)
		temp_2[0] = temp_1[0] + r*(temp_1[1] - 2*temp_1[0] + left_elem)
	else:
		comm.send(temp_1[block_size-1], dest = rank+1, tag = time_step)
		comm.send(temp_1[0],dest = rank-1, tag = time_step)
		left_elem = comm.recv(source = rank -1, tag = time_step)
		right_elem = comm.recv(source = rank+1,tag = time_step)
		temp_2[block_size-1] = temp_1[block_size-1] + r*(right_elem - 2*temp_1[block_size-1]+ temp_1[block_size-2])
		temp_2[0] = temp_1[0] + r*(temp_1[1] - 2*temp_1[0] + left_elem)
	temp_1 = temp_2 
	time_step += 1
	comm.Gather(temp_1,temp_arr,root =0)

	if rank ==0:
#		with open("Temperature_Profile.csv", "a") as myfile:
#		 	np.savetxt(myfile, temp_arr, fmt='%1.4e')
		temp_csv = np.reshape(temp_arr,(1,size_list))
		with open("Temperature_Profile.txt", "a") as myfile:
		 	np.savetxt(myfile, temp_csv, fmt='%1.4e', delimiter=",")
#			np.savetxt("Temp.csv",temp_csv, delimiter=",")
		 	#myfile.write("appended text")

#    	
#	if rank ==0:
#		np.savetxt('Temperature_Profile.out', temp_arr, fmt='%1.4e')
#	if rank==size-1:
#		print temp_2
#temp_arr[size_list-1] = 500
#while time <= time_max:
#end
