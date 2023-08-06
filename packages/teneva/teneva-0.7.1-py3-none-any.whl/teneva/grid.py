import itertools
import numpy as np


def ind2poi(I, a, b, n):
    """Transforms multiindices (samples) into points of the uniform grid."""
    if isinstance(a, list): a = np.array(a)
    if isinstance(b, list): b = np.array(b)
    if isinstance(n, list): n = np.array(n)

    if len(I.shape) == 1:
        # If we have only one multiindex
        t = I * 1. / (n - 1)
        x = t * (b - a) + a
        return x

    A = np.repeat(a.reshape((1, -1)), I.shape[0], axis=0)
    B = np.repeat(b.reshape((1, -1)), I.shape[0], axis=0)
    N = np.repeat(n.reshape((1, -1)), I.shape[0], axis=0)
    T = I * 1. / (N - 1)
    X = T * (B - A) + A
    return X


def ind2str(i):
    """Transforms array of int like [1, 2, 3] into string like '1-2-3'."""
    return '-'.join([str(int(v)) for v in i])


def lhs(shape, samples):
    d = len(shape)
    indices = np.empty((samples, d), dtype=int)
    for i, sh in enumerate(shape):
        part1 = np.repeat(np.arange(sh), samples // sh)
        part2 = np.random.choice(sh, samples-len(part1), replace=False)
        indices[:, i] = np.concatenate([part1, part2])
        np.random.shuffle(indices[:, i])
    return indices


def str2ind(s):
    """Transforms string like '1-2-3' into array of int like [1, 2, 3]."""
    return np.array([int(v) for v in s.split('-')], dtype=int)


def tt_sample(shape, k):
    def one_mode(sh1, sh2, rng):
        res = []
        if len(sh2) == 0:
            lhs_1 = lhs(sh1, k)
            for n in range(rng):
                for i in lhs_1:
                    res.append(np.concatenate([i, [n]]))
            len_1, len_2 = len(lhs_1), 1
        elif len(sh1) == 0:
            lhs_2 = lhs(sh2, k)
            for n in range(rng):
                for j in lhs_2:
                    res.append(np.concatenate([[n], j]))
            len_1, len_2 = 1, len(lhs_2)
        else:
            lhs_1 = lhs(sh1, k)
            lhs_2 = lhs(sh2, k)
            for n in range(rng):
                for i, j in itertools.product(lhs_1,  lhs_2):
                    res.append(np.concatenate([i, [n], j]))
            len_1, len_2 = len(lhs_1), len(lhs_2)
        return res, len_1, len_2

    idx = [0]
    idx_many = []
    pnts_many = []

    for i in range(len(shape)):
        pnts, len_1, len_2 = one_mode(shape[:i], shape[i+1:], shape[i])
        pnts_many.append(pnts)
        idx.append(idx[-1] + len(pnts))
        idx_many.append(len_2)

    return np.vstack(pnts_many), np.array(idx), np.array(idx_many)
