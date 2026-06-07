# How difficult is it to predict NRL?
# Compute Shannon entropy of the question of who wins
# the next match (unspecified distinct teams, neutral venue).

import numpy as np
from predict import prob
import matplotlib.pyplot as plt

posterior_sample = np.loadtxt("posterior_sample.txt")
H = []
pmax = []
num_teams = posterior_sample.shape[1] - 7

for i in range(num_teams):
    for j in range(i):
        p = prob(i, j, posterior_sample, neutral=True)
        p = np.array([p, 1.0 - p])
        pmax.append(np.max(p))
        H.append(-np.sum(p*np.log(p + 1E-300)/np.log(2.0)))
        print(i, j, flush=True)
print(f"{np.mean(H)} bits.")

plt.hist(pmax, 100)
plt.xlabel("Winning Probability of Favourite")
plt.show()
