import matplotlib.pyplot as plt

x = [1,5,10,25,50,100]
y = []

f = open("../logs/without_option/1_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/without_option/5_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/without_option/10_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/without_option/25_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/without_option/50_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/without_option/100_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)


plt.plot(x,y,label="Without Option")



x = [1,5,10,25,50,100]
y = []

f = open("../logs/with_option/1_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/with_option/5_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/with_option/10_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/with_option/25_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/with_option/50_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)

f = open("../logs/with_option/100_customers/response_times.txt", "r") 
lines = f.readlines()
f.close() 

tot = 0
num = 0
for line in lines:
	line = line.strip() 
	if line != '':
		num += 1
		tot += float(line)
y.append(tot/num)
plt.plot(x,y,label="With Option")
plt.legend()
plt.title('Response time VS. Concurrent Ingestions')
plt.xlabel('Number of users')
plt.ylabel('Response time')
plt.show()
