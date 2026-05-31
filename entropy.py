# How difficult is it to predict NRL?
# Compute Shannon entropy of the question of who wins
# the next match (unspecified distinct teams, neutral venue).

import numpy as np
from predict import prob

posterior_sample = np.loadtxt("posterior_sample.txt")
H = []

for i in range(17):
    for j in range(i):
        p = prob(i, j, posterior_sample, neutral=True)
        H.append(-p*np.log(p) - (1.0 - p)*np.log(1.0 - p))
        print(i, j, flush=True)
print(np.mean(H))

