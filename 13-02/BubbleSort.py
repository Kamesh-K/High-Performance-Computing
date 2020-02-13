import random 
random_list = []
random.seed(3)
size_list = 10
for i in range(size_list):
	random_number = random.randint(1,40)
	random_list.append(random_number)
print(random_list)
sorted = 0
iter = 1
while sorted==0 and iter < 40:
	sorted = 1
	iter += 1	
	for i in range(len(random_list)-1):
		if random_list[i] > random_list[i+1]:
			temp = random_list[i+1]
			random_list[i+1] = random_list[i]
			random_list[i] = temp
	print(random_list)	
	for i in range(len(random_list)-1):
		if random_list[i] > random_list[i+1]:
			sorted = 0	
print(iter)
