# Program to simulate a random walk process using Reflective boundary condition
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
# Declaing the variables used in the code 
nProcs = comm.Get_size()
n = nProcs
P = 24
del_x = 0.4 	# Step size used for computation 
random.seed(2)
class particle:
	pId = None 
	loc = 0
	def __init__(self,pId,loc):
		self.pId = pId 
		self.loc = loc 
pList = []		# Declaring the list of particles for the process 
nParticles = int(P/nProcs) # Number of particles present in the process 
# Initializing the particles with an ID and location 
for i in range(nParticles):
	loc = np.random.random()
	pList.append(particle(i+rank*nParticles,loc))
# Declaring the number of iterations to which the random walk is to be carried out 
iter = 1
iter_max = 100
# Displaying the number of particles present in each process before random walk 
print("Number of particles in rank {} = {}").format(rank,len(pList))
open('Particle_Track.txt', 'w').close()	
# Iteration for random walk begins
while iter <= iter_max:
	# Declaring the number for particles to be shifted to left and right process 
	particle_left = 0
	particle_right = 0
	nParticles = len(pList)
	# Discplacing the particles by a random number 
	for i in range(nParticles):
		displace = (np.random.random()-0.5)*del_x
		pList[i].loc += displace
	pop_list = []
	# Checking whether the particles are still in the range of the process domain 
	for i in range(len(pList)):
		if pList[i].loc <0:
			if rank == 0:
				pList[i].loc = -1*pList[i].loc 	# Reflective boundary condition 
			else: 
				particle_left+=1				# Incrementing particle to be shifted to left process by 1 
				pList[i].loc = 1-pList[i].loc 	# Initializing the new location in the left process 
				comm.send(pList[i],dest = rank-1, tag = (iter+2)**2) # Sending the particle to the left process 
				pop_list.append(i-len(pop_list))# Appending the pop list to remove from the current process 
		elif pList[i].loc >1:
			if rank==nProcs-1:
				pList[i].loc = 1 - pList[i].loc # Reflective boundary condition 
			else:
				particle_right+=1;
				pList[i].loc = pList[i].loc - 1 # Initializing the new location in the right process 
				comm.send(pList[i],dest = rank+1, tag = (iter+2)**2) # Sending the particle to the right process 
				pop_list.append(i-len(pop_list))# Appending the pop list to remove from the current process 
	for i in range(len(pop_list)):
		pList.pop(pop_list[i])					# Popping the data from the list 

	if rank == 0:
		comm.send(particle_right,dest = rank+1, tag = iter)						# Sending the number of particles to be sent to left process 
		particle_left = comm.recv(source = rank+1,tag = iter)					# Receiving number of particles to be received
		for i in range(particle_left):
			shifted_particle = comm.recv(source = rank+1,tag = (iter+2)**2)		# Sending the number of particle to right process
			pList.append(shifted_particle)										# Appending to the current particle list of process 
	elif rank == nProcs-1:
		comm.send(particle_left,dest=rank-1,tag = iter)							# Sending the number of particles to be sent to left process
		particle_right = comm.recv(source = rank-1,tag = iter)					# Receiving number of particles to be received
		for i in range(particle_right):
			shifted_particle = comm.recv(source = rank-1,tag = (iter+2)**2)
			pList.append(shifted_particle)
	else:
		comm.send(particle_right,dest = rank+1, tag = iter)						# Sending the number of particles to be sent to right process
		comm.send(particle_left,dest=rank-1,tag = iter)							# Sending the number of particles to be sent to left process
		particle_left = comm.recv(source = rank+1,tag = iter)
		for i in range(particle_left):
			shifted_particle = comm.recv(source = rank+1,tag = (iter+2)**2)		# Receiving number of particles to be received
			pList.append(shifted_particle)										# Appending to the current particle list of process 
		particle_right = comm.recv(source = rank-1,tag = iter)
		for i in range(particle_right):
			shifted_particle = comm.recv(source = rank-1,tag = (iter+2)**2)		# Receiving number of particles to be received
			pList.append(shifted_particle)										# Appending to the current particle list of process 
	iter+=1
	particle_found = 0
	nParticles = len(pList)						# Reinitializing the size of Particle list 
	for i in range(nParticles):
		if pList[i].pId == 0:
			with open('Particle_Track.txt', 'a') as f:
				print >> f, float((pList[i].loc)+float(rank))					# Writing the tracked value into the file
# Displaying the number of particles present in each process before random walk 				
print("Number of particles in rank {} = {}").format(rank,len(pList))	
