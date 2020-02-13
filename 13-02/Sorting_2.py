# Program to perform differnt sumations for findings the sum of first N natural numbers 
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
random_list = []
random.seed(3)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size
size_list = 8
if rank ==0:
	for i in range(size_list):
		random_number = random.randint(1,40)
		random_list.append(random_number)
	print(random_list)
sorted = 0
iter = 1
# Block Method
sorted = 1
# Spliting the array to processes
if rank ==0:
	for i in range(size_list):
		comm.send(random_list[i],dest = int(i/2),tag=0)
data_1 = comm.recv(source = 0, tag =0)
data_2 = comm.recv(source = 0, tag =0)
sorted = 0
while iter < 10 and sorted == 0:
#	print("Before Sorting - Iter - {} Rank {} - Elements - {} {}").format(iter,rank,data_1,data_2)	
	sorted = 1
	if iter%2 == 0:
		if data_1 > data_2:
			temp = data_2
			data_2 = data_1
			data_1 = temp
	else:	
		if rank == 0:
			comm.send(data_2, dest = 1, tag = iter)
		elif rank == n-1:
			comm.send(data_1,dest = n-2, tag = iter)
		else:			 
			comm.send(data_1,dest=rank-1, tag = iter)
			comm.send(data_2,dest=rank+1, tag = iter)

		if rank == 0:
			data_r = comm.recv(source = 1, tag = iter)
			if data_2 > data_r:			
				temp = data_2
				data_2 = data_r
				data_r = temp
		elif rank == n-1:
			data_l = comm.recv(source = n-2, tag = iter)
			if data_l > data_1: 
				temp = data_1
				data_1 = data_l
				data_l = temp
		else:			 
			data_l = comm.recv(source = rank-1, tag = iter)
			data_r = comm.recv(source = rank+1, tag = iter)
			if data_l > data_1: 
				temp = data_1
				data_1 = data_l
				data_l = temp
			if data_2 > data_r:			
				temp = data_2
				data_2 = data_r
				data_r = temp
	iter += 1
#	print("Rank {} - Elements - {} {}").format(rank,data_1,data_2)
	comm.send(data_1, dest = 0, tag = 0)
	comm.send(data_2, dest = 0, tag = 1)
	if rank ==0:
		for i in range(0,size_list,2):
			left = comm.recv(source = int(i/2),tag=0)
			right = comm.recv(source = int(i/2),tag=1)
			random_list[i] = left
			random_list[i+1] = right
		print random_list
		for i in range(len(random_list)-1):
			if random_list[i] > random_list[i+1]:
				sorted = 0
		comm.send(sorted,dest =0, tag = iter)		
		comm.send(sorted,dest = 1,tag=iter)
		comm.send(sorted,dest = 2,tag=iter)
		comm.send(sorted,dest = 3,tag=iter)
	sorted = comm.recv(source =0,tag =iter)
comm.send(data_1, dest = 0, tag = 0)
comm.send(data_2, dest = 0, tag = 1)
if rank ==0:
	for i in range(0,size_list,2):
		data_1 = comm.recv(source = int(i/2),tag=0)
		data_2 = comm.recv(source = int(i/2),tag=1)
		random_list[i] = data_1
		random_list[i+1] = data_2
	print "The Sorted Array is as follows:"
	print random_list

