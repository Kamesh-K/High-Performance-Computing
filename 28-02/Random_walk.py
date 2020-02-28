# Program to sort a solve the 1-D transient heat equation  
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
n = nProcs
P = 24
# Declaring the array and setting the seed for random
del_x = 1
random.seed(2)
class particle:
	pId = None 
	loc = 0
	def __init__(self,pId,loc):
		self.pId = pId 
		self.loc = loc 
pList = []
nParticles = int(P/nProcs)
for i in range(nParticles):
	loc = np.random.random()
	pList.append(particle(i+rank*nParticles,loc))
iter = 1
iter_max = 100
print("Number of particles in rank {} = {}").format(rank,len(pList))	
while iter < iter_max:
	particle_left = 0
	particle_right = 0
	nParticles = len(pList)
	for i in range(nParticles):
		displace = (np.random.random()-0.5)*del_x
		pList[i].loc += displace
	pop_list = []
	for i in range(len(pList)):
		if pList[i].loc <0:
			if rank == 0:
				pList[i].loc = -1*pList[i].loc
			else: 
				particle_left+=1
				pList[i].loc = 1-pList[i].loc
				comm.send(pList[i],dest = rank-1, tag = (iter+2)**2)
				pop_list.append(i)
		elif pList[i].loc >1:
			if rank==nProcs-1:
				pList[i].loc = 1 - pList[i].loc 
			else:
				particle_right+=1;
				pList[i].loc = pList[i].loc - 1
				comm.send(pList[i],dest = rank+1, tag = (iter+2)**2)
				pop_list.append(i)
	pList_new = []
	pop_list.append(-1)
	ptr_poplist = 0
	for i in range(len(pList)):
		if i != pop_list[ptr_poplist]:
			pList_new.append(pList[i])
		else:
			ptr_poplist+=1 
	pList = pList_new
	nParticles = len(pList)

	if rank == 0:
		comm.send(particle_right,dest = rank+1, tag = iter)
		particle_left = comm.recv(source = rank+1,tag = iter)
		for i in range(particle_left):
			shifted_particle = comm.recv(source = rank+1,tag = (iter+2)**2)
			pList.append(shifted_particle)
	elif rank == nProcs-1:
		comm.send(particle_left,dest=rank-1,tag = iter)
		particle_right = comm.recv(source = rank-1,tag = iter)
		for i in range(particle_right):
			shifted_particle = comm.recv(source = rank-1,tag = (iter+2)**2)
			pList.append(shifted_particle)
	else:
		comm.send(particle_right,dest = rank+1, tag = iter)
		comm.send(particle_left,dest=rank-1,tag = iter)
		particle_left = comm.recv(source = rank+1,tag = iter)
		for i in range(particle_left):
			shifted_particle = comm.recv(source = rank+1,tag = (iter+2)**2)
			pList.append(shifted_particle)
		particle_right = comm.recv(source = rank-1,tag = iter)
		for i in range(particle_right):
			shifted_particle = comm.recv(source = rank-1,tag = (iter+2)**2)
			pList.append(shifted_particle)
	iter+=1
	particle_found = 0
	nParticles = len(pList)
	for i in range(nParticles):
		if pList[i].pId == 0:
			bcast_rank = rank
			with open('Particle_Track.txt', 'a') as f:
				print >> f, float((pList[i].loc)+float(rank))
print("Number of particles in rank {} = {}").format(rank,len(pList))	
#for i in range(len(pList)):
#	print("Rank - {} - ID {} LOC - {}").format(rank, pList[i].pId,pList[i].loc)
