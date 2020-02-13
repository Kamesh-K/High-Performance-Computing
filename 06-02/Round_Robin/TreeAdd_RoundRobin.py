import math
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
N = 100
n= size
a = list(range(1,N+1))
sum = 0
if rank == 0:
	start1 = MPI.Wtime()
for i in range(1,N+1):
	if i%n == rank:
#		print("Rank {} - Sum = {} and Added Value = {}").format(rank,sum,i)		
		sum += i
#print("Rank {} - Sum = {}").format(rank,sum)
height = math.log(n,2)
curr_height = 1
data = sum 
if rank == 0:
	start2 = MPI.Wtime()
while curr_height < height:
	diff = 2**curr_height	
	points = list(np.arange(0,size,diff))
	curr_size = len(points)
	for i in range(curr_size):
		if rank == points[i] + diff/2:
			comm.send(data,dest = points[i],tag = curr_height)
		elif rank == points[i] and rank + diff/2 < size:
			data += comm.recv(source = rank + diff/2,tag=curr_height)
#			print("Rank {} - received data from Rank {} and updated data = {}").format(rank,rank +diff/2,data)	
	curr_height += 1
if rank == 2**(height-1):
	comm.send(data,dest = 0,tag=height)
if rank ==0:	
	data += comm.recv(source = 2**(height-1),tag=height)
	print("Total Sum = {}, For N = {}").format(data,N)
	end = MPI.Wtime()
	T_complete = end - start1 
	T_add = end - start2
	print("Total Time taken for calculation is = {} seconds").format(T_complete)
	print("Total Time taken for addition is = {} seconds").format(T_add)

