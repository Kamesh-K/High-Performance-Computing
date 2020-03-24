# Program to perform matrix multiplication
# Importing the required libraries
import math
import random
import numpy as np
from mpi4py import MPI
import seaborn as sns
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
size = nProcs
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
m = None
k = None
n = None

if rank == 0:
    A = np.random.rand(4, 6)
    B = np.random.rand(6, 6)
    print("Matrix A \n {}").format(A)
    print("Matrix B \n {}").format(B)
    m, k = np.shape(A)
    k, n = np.shape(B)
    C = np.full((m, n), 0.00)
# To factorize nProc so that iProcs/jProcs ~ iLength/jLength
m = comm.bcast(m, root=0)
n = comm.bcast(n, root=0)
k = comm.bcast(k, root=0)
if nProcs == 4:
    iProcs = 2
    jProcs = 2
elif nProcs == 6:
    if m > n:
        jProcs = 3
        iProcs = 2
    else:
        iProcs = 2
        jProcs = 3
iLength = m / iProcs
jLength = n / jProcs
# print("iProcs = {}, jProcs = {}").format(iProcs,jProcs)
if rank == 0:
    k = 0
    for i in range(0, iProcs):
        for j in range(0, jProcs):
            rows = A[i * iLength:(i + 1) * iLength, :]
            rows.tolist()
            cols = B[:, j * jLength:(j + 1) * jLength]
            comm.send(rows, dest=i * jProcs + j, tag=0)
            comm.send(cols, dest=i * jProcs + j, tag=0)
rows = None
cols = None
rows = comm.recv(source=0, tag=0)
cols = comm.recv(source=0, tag=0)
# print("Rows - {}, cols - {} for Rank - {}").format(rows,cols,rank)
ans = np.dot(rows, cols)
# print ans
comm.send(ans, dest=0, tag=0)
if rank == 0:
    final_ans = None
    for i in range(iProcs):
        row_ans = None
        for j in range(jProcs):
            segment = comm.recv(source=i * jProcs + j, tag=0)
            segment = np.asarray(segment)
            # print segment
            if j == 0:
                row_ans = segment
            else:
                row_ans = np.hstack((row_ans, segment))
            # print("RowAns - {} ").format(row_ans)
        if i == 0:
            final_ans = row_ans
        else:
            final_ans = np.vstack((final_ans, row_ans))
    print("Matrix C \n {}").format(final_ans)
    print("Matrix A * B using numpy \n {}").format(np.dot(A, B))
