import matplotlib.pyplot as plt


max_c=0
max_d=0

with open('../data/datav2/datav2/densityvscBahmaniLJ1600withETv2.txt') as file:
    bahmani_x_values=[]
    bahmani_y_values=[]
    for line in file:
        data=line.strip().split(" ")
        if float(data[1])>max_d:
            max_d=float(data[1])
            max_c=float(data[0])
        bahmani_x_values.append(float(data[0]))
        bahmani_y_values.append(float(data[1]))

print('maximum c for maximum density for bahmani: ',max_c)
max_c=0
max_d=0


with open('../data/datav2/datav2/densityvscOursLJ1600withETv2.txt') as file:
    our_x_values=[]
    our_y_values=[]
    for line in file:
        data=line.strip().split(" ")
        if float(data[1])>max_d:
        
            max_d=float(data[1])
            max_c=float(data[0])

        our_x_values.append(float(data[0]))
        our_y_values.append(float(data[1]))

print('maximum c for maximum density for ours: ',max_c)

plt.plot(bahmani_x_values, bahmani_y_values, color='green', label='bahmani')
plt.plot(our_x_values,our_y_values, color='red', label='ours')
#plt.xscale('log')
plt.xlabel('c values')
plt.ylabel('density')
plt.title('Live Journal')
plt.legend()
plt.savefig('LJdvsc1600noLog.png')