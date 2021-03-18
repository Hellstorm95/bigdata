f = open("data/general.log", "r")
lines = f.readlines()
f.close
runtime = 0
num = 0
for line in lines:
    line = line.split()
    if line[2] == "INFO":
        num += 1
        runtime += float(line[7])
         
runtime = runtime / num 

print("The general avg runtime is:" + str(runtime))

f = open("data/user1/user1.log", "r")
lines = f.readlines()
f.close
runtime = 0
num = 0
for line in lines:
    line = line.split()
    if line[2] == "INFO":
        num += 1
        runtime += float(line[7])
         
runtime = runtime / num 

print("The user1 avg runtime is:" + str(runtime))

f = open("data/user2/user2.log", "r")
lines = f.readlines()
f.close
runtime = 0
num = 0
for line in lines:
    line = line.split()
    if line[2] == "INFO":
        num += 1
        runtime += float(line[7])
         
runtime = runtime / num 

print("The user2 avg runtime is:" + str(runtime))
