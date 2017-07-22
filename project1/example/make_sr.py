import numpy as np

n = 40
a = np.arange(n)

with open("source.txt", "w") as f:
    for i in range(n):
        f.write("{:6.2f} {:6.2f}\n".format(a[i], 1))
    for i in range(n):
        f.write("{:6.2f} {:6.2f}\n".format(1, a[i]))

with open("receiver.txt", "w") as f:
    for i in range(n):
        f.write("{:6.2f} {:6.2f}\n".format(a[i], n-1))
    for i in range(n):
        f.write("{:6.2f} {:6.2f}\n".format(n-1, a[i]))
