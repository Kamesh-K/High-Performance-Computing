from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ping_pong_count=-1;
ping_pong_count=ping_pong_count+1
comm.send(ping_pong_count,dest=1,tag=11)
ping_pong_max = 10
while ping_pong_count < 10:
	if rank == 0:
		dest_rank=1;
		ping_pong_count = comm.recv(source=1,tag=11)
		print("{} received ping pong count = {} from {}").format(int(0),ping_pong_count,int(1))	
		ping_pong_count=ping_pong_count+1
		print("{} sent and incremented ping pong count = {} to {}").format(int(0),ping_pong_count,int(1))		
		comm.send(ping_pong_count,dest=1,tag=11)	
	elif rank ==1:	
		dest_rank=0;
		ping_pong_count = comm.recv(source=0,tag=11)
		print("{} received ping pong count = {} from {}").format(int(1),ping_pong_count,int(0))	
		ping_pong_count=ping_pong_count+1		
		print("{} sent and incremented ping pong count = {} to {}").format(int(1),ping_pong_count,int(0))
		comm.send(ping_pong_count,dest=0,tag=11)
		

