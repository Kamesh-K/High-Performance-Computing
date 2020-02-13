import math
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
data = 1
#N = 100
N = 100
n=4
a = list(range(1,N+1))
sum = 0
if rank == 0:
	start = MPI.Wtime()
for i in range(1,N+1):
	if i%n == rank:
#		print("Rank {} - Sum = {} and Added Value = {}").format(rank,sum,i)		
		sum += i
print("Rank {} - Sum = {}").format(rank,sum)
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

height = math.log2(n)
while height>0:
	height -=1
	tree_length = 1
	my_rank = rank / 2
	comm.recv(source=my_rank*tree_length)
	
