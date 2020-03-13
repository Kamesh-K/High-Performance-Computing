### Matrix Multiplication using MPI4py

The given matrix  A is decomposed into different processes and the matrix multiplication is carried out in different processes. 

The rows of A is stored in the first iProcs and the columns in the jProcs 

The division follows the following rule:
$$
AR = iLength/jLength \\
C = ceil(\sqrt(AR*nProcs))\\
if AR >1, we\ have - \\
C = ceil(\sqrt(\frac{1}{AR}*nProcs))
$$
And we obtain:
$$
iProc = C\  \& \ jProc = (N/C) 
$$
