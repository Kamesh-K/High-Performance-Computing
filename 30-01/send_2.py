from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank == 0:
	data = {'a':7,'b':3.14}
	print 'Printing Data'
	print data
	comm.send(data,dest=1,tag=11)
elif rank == 1:
	data = (1,2,3,4)
	print 'Before receiving data!' 
	print data
	print type(data) 
	print 'Receiving Data'
	data = comm.recv(source=0,tag=11)
	print 'After receiving data!' 	
	print data
	print type(data)
#elif rank == 2:
#	data = {'a':6,'b':4}
#	comm.send(data,dest=4,tag=13)
#elif rank == 3:
#	data = comm.recv(source=3,tag=13)
#	print data 

