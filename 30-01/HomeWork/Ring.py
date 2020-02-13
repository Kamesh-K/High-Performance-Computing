from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
data = 1
comm.send(data,dest=1,tag=11)
max_ring_size = 4
source_rank=(rank+max_ring_size-1)%max_ring_size
dest_rank=(rank+1)%max_ring_size
data = comm.recv(source=source_rank,tag=11)	
print("{} received data = {} from {}").format(rank,data,source_rank)	
print("{} sent and data = {} to {}").format(rank,data,dest_rank)		
comm.send(data,dest=dest_rank,tag=11)
