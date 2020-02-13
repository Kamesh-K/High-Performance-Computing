from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ping_pong_count=-1;
comm.send(ping_pong_count,dest=1,tag=11)
source_rank=(rank+1)%2
dest_rank=(rank)%2
ping_pong_max = 10
while ping_pong_count < ping_pong_max:
	ping_pong_count = comm.recv(source=source_rank,tag=11)	
	print("{} received ping pong count = {} from {}").format(source_rank,ping_pong_count,dest_rank)	
	ping_pong_count=ping_pong_count+1
	print("{} sent and incremented ping pong count = {} to {}").format(source_rank,ping_pong_count,dest_rank)		
	comm.send(ping_pong_count,dest=source_rank,tag=11)		

