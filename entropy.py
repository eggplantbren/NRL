# How difficult is it to predict NRL?
# Compute Shannon entropy of the question of who wins
# the next match (unspecified distinct teams, neutral venue).

import numpy as np
from predict import prob
import matplotlib.pyplot as plt

posterior_sample = np.loadtxt("posterior_sample.txt")
H = []
pmax = []

for i in range(17):
    for j in range(i):
        p = prob(i, j, posterior_sample, neutral=True)
        p = np.array([p, 1.0 - p])
        pmax.append(np.max(p))
        H.append(-np.sum(p*np.log(p + 1E-300)))
        print(i, j, flush=True)
print(np.mean(H))

plt.hist(pmax, 100)
plt.xlabel("Winning Probability of Favourite")
plt.show()
