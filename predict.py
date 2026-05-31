import numpy as np
from scipy.stats import t
import sys


def prob(team1, team2, posterior_sample, neutral=False):
    abilities = posterior_sample[:, -17:]
    probs = np.empty(abilities.shape[0])
    for i in range(abilities.shape[0]):
        home_bonus = posterior_sample[i, 0]
        if neutral:
            home_bonus = 0.0

        loc = home_bonus + abilities[i, team1] \
                - abilities[i, team2]
        shape = posterior_sample[i, 1]
        scale = posterior_sample[i, 2]
        probs[i] = 1.0 - t.cdf(0.0, df=shape, loc=loc, scale=scale)
    return np.mean(probs)



if __name__ == "__main__":

    # Build team lookup
    lookup = dict()
    with open("teams.txt") as f:
        for line in f:
            parts = line.split(" ")
            lookup[parts[-1][0:-1].lower()] = int(parts[0])
    f.close()

    neutral = "--neutral" in sys.argv
    assert(len(sys.argv) >= 3)
    teams = [lookup[name.lower()] for name in sys.argv[-2:]]
    posterior_sample = np.loadtxt("posterior_sample.txt")
    print(prob(teams[0], teams[1], posterior_sample, neutral=neutral))

