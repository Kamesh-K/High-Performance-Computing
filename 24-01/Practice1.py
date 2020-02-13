from mpi4py import MPI
comm = MPI.COMM_WORLD
print "Hello World from Rank ",comm.Get_rank(), "of total processors ",comm.Get_size() 
comm.barrier()

