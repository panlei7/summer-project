import numpy as np

d = 5
n = 140
a = np.arange(0, n, d)
m = 180
b = np.arange(0, m, d)


with open("source.txt", "w") as f:
    for i in range(int(n/d)):
        f.write("{:6.2f} {:6.2f}\n".format(a[i], 1))
    for i in range(int(m/d)):
        f.write("{:6.2f} {:6.2f}\n".format(1, b[i]))

with open("receiver.txt", "w") as f:
    for i in range(int(n/d)):
        f.write("{:6.2f} {:6.2f}\n".format(a[i], m-1))
    for i in range(int(m/d)):
        f.write("{:6.2f} {:6.2f}\n".format(n-1, b[i]))
