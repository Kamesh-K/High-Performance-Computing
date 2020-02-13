import math
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
data = 1
N=100
#N = 100000000
n = size
sum = 0
block_size = int(math.ceil(float(N)/float(n)))
limit =(rank+1)*block_size+1
limit = min(limit,N+1)
if rank == 0:
	start = MPI.Wtime()
for i in range(rank*block_size+1,limit):
#	print("Rank {} - Sum = {} and Added Value = {}").format(rank,sum,i)		
	sum += i
#print("Rank {} - Sum = {}").format(rank,sum)
if rank == 0:
	for i in range(1,n):
		data = comm.recv(source=i,tag=11)
		sum += data 
	print("Total Sum = {}, For N = {}").format(sum,N)
else: 
	comm.send(sum,dest=0,tag=11)
if rank == 0:
	end = MPI.Wtime()
	T = end - start 
	print("Total Time taken for calculation is = {}").format(T)
