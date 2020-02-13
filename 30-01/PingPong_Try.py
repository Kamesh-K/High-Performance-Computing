from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ping_pong_count=-1;
comm.send(ping_pong_count,dest=1,tag=11)
source_rank=0;
dest_rank=1;
while ping_pong_count < 10:
		ping_pong_count = comm.recv(source=source_rank,tag=11)
		ping_pong_count=ping_pong_count+1
		#print ("From RANK 0 - After receiving ",ping_pong_count)
		#print("Ping from ",ping_pong_count," from Rank ",rank)
		#print ("From RANK 0 - before sending ",ping_pong_count)
		print("{} sent and incremented ping pong count {} to {}").format(source_rank,ping_pong_count,dest_rank)		
		comm.send(ping_pong_count,dest=dest_rank,tag=11)		
		source_rank=rank
		dest_rank=rank		
	
