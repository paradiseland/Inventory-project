from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.pyplot as plt

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
print(kde.score_samples(X))

plt.plot(kde.score_samples(X))
plt.show()
# array([-0.41075698, -0.41075698, -0.41076071, -0.41075698, -0.41075698,
#        -0.41076071])
