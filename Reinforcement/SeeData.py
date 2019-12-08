import numpy as np

# np.nonzero(np.load('./Reinforcement/QTable.npy'))

data = np.load('./QTable.npy')

print(np.shape(data))
printArr = []
for row in range(400):
    for col in range(499):
        print(row,col)
        printArr.append(data[row,col])
print(printArr)
# np.savetxt("foo.csv", data, fmt='%1.4e', delimiter=",")
