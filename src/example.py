import numpy as np
import matplotlib.pyplot as plt

def collatz_func(x):
    x_list = []
    x_list.append(x)
    while x > 1:
        if x % 2 == 0:
            x /= 2
        else:
            x = 3*x + 1
        x_list.append(x)
    return x_list

x0_list = np.arange(1, 100)

list_list = []

for l in x0_list:
    list0 = collatz_func(l)
    list_list.append(list0)
    plt.plot(list0)

plt.grid()
plt.savefig('./figures/collatz.png')