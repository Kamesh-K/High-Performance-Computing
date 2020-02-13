from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ping_pong_count=-1;
comm.send(ping_pong_count,dest=1,tag=11)
while ping_pong_count < 10:
	if rank == 0:
		ping_pong_count = comm.recv(source=1,tag=11)
		ping_pong_count=ping_pong_count+1
		#print ("From RANK 0 - After receiving ",ping_pong_count)
		print("Ping from ",ping_pong_count," from Rank ",rank)
		#print ("From RANK 0 - before sending ",ping_pong_count)
		comm.send(ping_pong_count,dest=1,tag=11)	
	elif rank ==1:	
		ping_pong_count = comm.recv(source=0,tag=11)
		#print ("From RANK 1 - After Receiving ",ping_pong_count)		
		ping_pong_count=ping_pong_count+1		
		print("Pong from ",ping_pong_count," from Rank ",rank)
		comm.send(ping_pong_count,dest=0,tag=11)
		

