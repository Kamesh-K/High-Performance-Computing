## Class on 06-02 

**Pickle for Memory Serialization**

CPickle is also there for Python 2 

In python 3, its integrated in Pickle

```python
from mpi4py import MPI
comm = MPI.COMM_WORLD
comm.send(a)
comm.Send(a)
```

This creates a bufferable object in python

Send is used to transfer bufferable objects in python whereas send is used for general python objects 

Home Work for today is to code the Tree Structure implementation of Addition and compare the Wall time of all the processes and report which of them is better and possibly why 

##### Send and Receive Arbitary (n) size of Data !

##### Using Status Command for Sharing objects:

###### Using Probe command 

```python
from mpi4py import MPI
import numpy as np
import pickle
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
	data = rank*np.ones(3,dtype= np.float64)
	print data
	comm.Send([data,MPI.DOUBLE],dest=1,tag=1)
if rank ==1:
	info = MPI.Status()
	comm.Probe(MPI.ANY_SOURCE,MPI.ANY_TAG,info)
	source = info.Get_source()
	tag = info.Get_tag()
	count = info.Get_elements(MPI.DOUBLE)
	size = info.Get_count()
	print('On {} Source - {}, tag - {}, count -{}, size-{}').format(rank,source,tag,count,size)
	
```

Probe Command is used to obtain the details of the data being Sent to the process. 

###### Using Receive command

```python
from mpi4py import MPI
import numpy as np
import pickle
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = rank*np.ones(3,dtype= np.float64) # Note the Variable needs to be declared in this case 
print data
if rank == 0:
	comm.Send([data,MPI.DOUBLE],dest=1,tag=1)
if rank ==1:
	info = MPI.Status()
	comm.Recv(data,MPI.ANY_SOURCE,MPI.ANY_TAG,info)
	source = info.Get_source()
	tag = info.Get_tag()
	count = info.Get_elements(MPI.DOUBLE)
	size = info.Get_count()
	print('On {} Source - {}, tag - {}, count -{}, size-{}, data-{}').format(rank,source,tag,count,size,data)
```

### Class on 07-02 

```python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank ==0:
    	data = {'key1' : [7,2.72,2+3j],
                'key2' : ('abc','xyz')}
else:
        data = None
data = comm.bcast(data,root=0)
print(data,rank)
```

```python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = (rank+1)**2
data = comm.gather(data,root=0)
if rank == 0:
	for i in range(size):
        assert data[i] == (i+1)**2
else 
	assert data is None
if rank == 0:
    print(data)
```

```
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank ==0:
	data = [(i+1)**2 for i in range(size)]
else:
	data = None
data = comm.scatter(data,root=0)
assert data == (rank+1)**2	
#print("Data = {}, Rank = {}").format(data,rank)

```

