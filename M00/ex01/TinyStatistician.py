import numpy as np
import math

class TinyStatistician():

    def mean(self, x):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        res = 0
        for elem in x:
            res += elem
        res /= (x.shape[0])
        return res

    def median(self, x):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        x.sort()
        if x.shape[0] % 2 == 0:
            ind_min = int((x.shape[0] - 1) / 2)
            ind_max = int(x.shape[0] / 2)
            res = (x[ind_max] + x[ind_min]) / 2
            return res
        ind = int((x.shape[0] - 1) / 2)
        return float(x[ind])

    def quartile(self, x):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        x.sort()
        if (x.shape[0] / 4) % 2 == 0:
            first_ind = int((x.shape[0] - 1) / 4)
        else:
            first_ind = int((x.shape[0]) / 4)
        if (x.shape[0] * 3 / 4) % 2 == 0:
            third_ind = int(((x.shape[0] - 1) * 3) / 4)
        else:
            third_ind = int(((x.shape[0]) * 3) / 4)
        return [float(x[first_ind]), float(x[third_ind])]

    def percentile(self, x, p):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        elif not isinstance(p, int) or p > 100 or p <= 0:
            print("Percentile is incompatible")
            return None
        x.sort()
        if (x.shape[0] * p / 100) % 2 == 0:
            per_ind = int((x.shape[0] - 1) * p / 100)
        else:
            per_ind = int(x.shape[0] * p / 100)
        return float(x[per_ind])

    def var(self, x):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        mean = self.mean(x)
        res = 0
        for elem in x:
            res += (elem - mean) ** 2
        res /= x.shape[0]
        return res

    def std(self, x):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            print("Input is not a numpy array of dimension 1")
            return None
        var = self.var(x)
        return math.sqrt(var)


ts = TinyStatistician()
a = np.array([1, 42, 300, 10, 59])
print(ts.mean(a))
print(ts.median(a))
print(ts.quartile(a))
print(ts.percentile(a, 10))
print(ts.percentile(a, 28))
print(ts.percentile(a, 83))
print(ts.var(a))
print(ts.std(a))