# Program to solve a 2-D couette flow of fluid 
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
import seaborn as sns
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
size = nProcs
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
# Declaring the array and setting the seed for random
# del_x = 0.025
# del_y = 0.025
del_x = 0.0025
del_y = 0.0025
del_t = 0.1 
length = 0.2
time_max = 1000
alpha = 10**(-4)
r = alpha * del_t /(del_x**2)
size_list = int(length/(del_x*(nProcs)**0.5))
side_size = int(length/(del_x))
block_size = size_list*size_list
local_temp = np.full((size_list,size_list),0.00)
temp_1 = local_temp
temp_2 = local_temp
if rank == 0:
	local_temp[:,0]= 300.00
	local_temp[0,:] = 400.00
elif rank == 1:
	local_temp[:,size_list-1] = 100
	local_temp[0,:] = 400.00
elif rank == 2:
	local_temp[:,0] = 300.00
else :
	local_temp[:,size_list-1] = 100.00
global_temp = None
local_temp = np.reshape(local_temp,(1,block_size))
# print(local_temp)
local_temp.tolist()
comm.send(local_temp, dest=0, tag=rank**2)
open('Temperature_Profile.txt', 'w').close()	
# print(local_temp)
comm.barrier()
if rank == 0:
	# print "Printing the Received buffer"
	local_temp_0 = None 
	local_temp_1 = None
	local_temp_2 = None
	local_temp_3 = None
	local_temp_0 = comm.recv(source=0, tag=0)
	local_temp_1 = comm.recv(source=1, tag=1)
	local_temp_2 = comm.recv(source=2, tag=4)
	local_temp_3 = comm.recv(source=3, tag=9)
	local_temp_0 = np.asarray(local_temp_0)
	local_temp_1 = np.asarray(local_temp_1)
	local_temp_2 = np.asarray(local_temp_2)
	local_temp_3 = np.asarray(local_temp_3)
	local_temp_0 = np.reshape(local_temp_0,(size_list,size_list))
	local_temp_1 = np.reshape(local_temp_1,(size_list,size_list))
	local_temp_2 = np.reshape(local_temp_2,(size_list,size_list))
	local_temp_3 = np.reshape(local_temp_3,(size_list,size_list))
	# print(local_temp_0)
	# print(local_temp_1)
	# print(local_temp_2)
	# print(local_temp_3)
	global_hor_1 = np.hstack((local_temp_0,local_temp_1))
	global_hor_2 = np.hstack((local_temp_2,local_temp_3))
	global_temp = np.vstack((global_hor_1,global_hor_2))
	# print global_temp
	global_temp.tolist()
global_temp = comm.bcast(global_temp,root=0)
global_temp = np.asarray(global_temp)
global_temp = np.reshape(global_temp,(size_list*2,size_list*2))
if rank ==0:
	print global_temp
comm.barrier()
origin_shift_x = 0
origin_shift_y = 0
if rank == 1:
	origin_shift_y = size_list
elif rank == 2:
	origin_shift_x = size_list
elif rank == 3:
	origin_shift_x = size_list
	origin_shift_y = size_list
else:
	origin_shift_y = 0
	origin_shift_x = 0
local_temp = np.reshape(local_temp,(size_list,size_list))
# print("Printing local Temp - {}").format(local_temp)
# print np.shape(global_temp)
time_iter = 1
while time_iter <= 1:
	diff_temp = np.full((size_list,size_list),0.00)
	for i in range(size_list):
		for j in range(size_list):
			x = origin_shift_x + i
			y = origin_shift_y + j
			if x == 0 or y == 0 or y == side_size-1:
				diff_temp[i,j] = 0
			elif x == side_size-1:
				diff_temp[i,j] = r*(global_temp[x,y+1] + global_temp[x,y-1] + 2*global_temp[x-1,y] - 4 * global_temp[x,y])/4 
			elif x>=0 and y>=0 and x<side_size and y<side_size:
				diff_temp[i,j] = r*(global_temp[x+1,y] + global_temp[x,y+1] + global_temp[x,y-1] + global_temp[x-1,y] - 4 * global_temp[x,y])/4
			else:
				print("Index out of bounds - x - {} y - {} i - {} j - {} rank - {}").format(x,y,i,j,rank) 
	local_temp = np.add(local_temp,diff_temp)
	# print("Rank = {}, local temp - {}").format(rank,local_temp)
	local_temp.tolist()
	comm.send(local_temp, dest=0, tag=rank**2)
	# print(local_temp)
	comm.barrier()
	if rank == 0:
		# print "Printing the Received buffer"
		local_temp_0 = None 
		local_temp_1 = None
		local_temp_2 = None
		local_temp_3 = None
		local_temp_0 = comm.recv(source=0, tag=0)
		local_temp_1 = comm.recv(source=1, tag=1)
		local_temp_2 = comm.recv(source=2, tag=4)
		local_temp_3 = comm.recv(source=3, tag=9)
		local_temp_0 = np.asarray(local_temp_0)
		local_temp_1 = np.asarray(local_temp_1)
		local_temp_2 = np.asarray(local_temp_2)
		local_temp_3 = np.asarray(local_temp_3)
		local_temp_0 = np.reshape(local_temp_0,(size_list,size_list))
		local_temp_1 = np.reshape(local_temp_1,(size_list,size_list))
		local_temp_2 = np.reshape(local_temp_2,(size_list,size_list))
		local_temp_3 = np.reshape(local_temp_3,(size_list,size_list))
		# print(local_temp_0)
		# print(local_temp_1)
		# print(local_temp_2)
		# print(local_temp_3)
		global_hor_1 = np.hstack((local_temp_0,local_temp_1))
		global_hor_2 = np.hstack((local_temp_2,local_temp_3))
		global_temp = np.vstack((global_hor_1,global_hor_2))
		# print global_temp
		global_temp.tolist()
	global_temp = comm.bcast(global_temp,root=0)
	global_temp = np.asarray(global_temp)
	global_temp = np.reshape(global_temp,(size_list*2,size_list*2))
	local_temp = np.asarray(local_temp)
	local_temp = np.reshape(local_temp,(size_list,size_list))
	time_iter += 1
if rank ==0:
	print global_temp
	plot_temp = sns.heatmap(global_temp)
	fig = plot_temp.get_figure()
	fig.savefig("time_iter.png")
	fig.clf()
	temp_csv = np.reshape(global_temp,(1,side_size**2))
	with open("Temperature_Profile.txt", "a") as myfile:
	 	np.savetxt(myfile, temp_csv, fmt='%1.4e', delimiter=",")








# print global_temp

# vel_arr = None
# velocity = 5.0
# block_size = int(size_list/size)
# local_vel_arr = np.empty(block_size).fill(0)
# open('Temperature_Profile.txt', 'w').close()	
# sendbuf = None
# if rank == 0:
#     vel_arr = np.empty([size, block_size], dtype='f')
#     vel_arr.T[:,:] = 0
#     vel_arr[size-1,block_size-1] = velocity
# local_vel_arr = np.empty(block_size, dtype='f')
# comm.Scatter(vel_arr, local_vel_arr, root=0)
# u_1 = local_vel_arr
# u_2 = local_vel_arr
# max_time_step = int(time_max/del_t)
# time_step = 0 
# left_elem = None 
# right_elem = None 
# while time_step < max_time_step:
# 	for i in range(1,block_size-1):
# 		u_2[i]= u_1[i] + r*(u_1[i+1] - 2*u_1[i] + u_1[i-1])
# 	if rank == 0:
# 		comm.send(u_1[block_size-1], dest = rank+1, tag = time_step)
# 		right_elem = comm.recv(source = rank+1,tag = time_step)
# 		u_2[block_size-1] = u_1[block_size-1] + r*(right_elem - 2*u_1[block_size-1]+ u_1[block_size-2])
# 	elif rank == size - 1:
# 		comm.send(u_1[0],dest = rank-1, tag = time_step)
# 		left_elem = comm.recv(source = rank -1, tag = time_step)
# 		u_2[0] = u_1[0] + r*(u_1[1] - 2*u_1[0] + left_elem)
# 	else:
# 		comm.send(u_1[block_size-1], dest = rank+1, tag = time_step)
# 		comm.send(u_1[0],dest = rank-1, tag = time_step)
# 		left_elem = comm.recv(source = rank -1, tag = time_step)
# 		right_elem = comm.recv(source = rank+1,tag = time_step)
# 		u_2[block_size-1] = u_1[block_size-1] + r*(right_elem - 2*u_1[block_size-1]+ u_1[block_size-2])
# 		u_2[0] = u_1[0] + r*(u_1[1] - 2*u_1[0] + left_elem)
# 	u_1 = u_2 
# 	time_step += 1
# 	comm.Gather(u_1,vel_arr,root =0)

# 	if rank ==0:
# 		vel_csv = np.reshape(vel_arr,(1,size_list))
# 		with open("Velocity_Profile.txt", "a") as myfile:
# 		 	np.savetxt(myfile, vel_csv, fmt='%1.4e', delimiter=",")
