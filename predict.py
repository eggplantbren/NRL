import numpy as np
from scipy.stats import t
import sys


posterior_sample = np.loadtxt("posterior_sample.txt")

if __name__ == "__main__":

    neutral = "--neutral" in sys.argv
    teams = [int(i) for i in sys.argv[-2:]]
    assert(len(teams) == 2)

    abilities = posterior_sample[:, -17:]
    probs = np.empty(abilities.shape[0])
    for i in range(abilities.shape[0]):
        home_bonus = posterior_sample[i, 0]
        if neutral:
            home_bonus = 0.0

        loc = home_bonus + abilities[i, teams[0]] \
                - abilities[i, teams[1]]
        shape = posterior_sample[i, 1]
        scale = posterior_sample[i, 2]
        probs[i] = 1.0 - t.cdf(0.0, df=shape, loc=loc, scale=scale)
    print(np.mean(probs))
