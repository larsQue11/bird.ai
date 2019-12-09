import numpy as np

# data = np.nonzero(np.load('./QTable.npy'))

data = np.load('./QTable.npy')

print(np.shape(data))
printArr = []
# for row in range(400):
#     for col in range(499):
#         print(row,col)
#         printArr.append(data[row,col])
# print(printArr)

for row in data:
    for col in row:
        np.savetxt("foo.csv", row, fmt='%1.4e', delimiter=",")
