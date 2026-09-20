"""Exact clipped integration of piecewise linear supported intervals, seconds/ugy/h."""
import numpy as np


class Stream:
    def __init__(self, t, v, max_gap=300):
        self.t, self.v = np.asarray(t, float), np.asarray(v, float)
        dt = np.diff(self.t)
        valid = (dt > 0) & (dt <= max_gap) & np.isfinite(self.v[:-1]) & np.isfinite(self.v[1:])
        self.left, self.right = self.t[:-1][valid], self.t[1:][valid]
        self.a, self.b = self.v[:-1][valid], self.v[1:][valid]
        self._prepare()

    @classmethod
    def segments(cls, left, right, a, b):
        obj = cls([], [])
        obj.left, obj.right, obj.a, obj.b = map(lambda x: np.asarray(x, float), (left, right, a, b))
        obj._prepare()
        return obj

    def _prepare(self):
        self.area = np.r_[0, np.cumsum((self.a+self.b)*.5*(self.right-self.left)/3600)]
        self.support = np.r_[0, np.cumsum(self.right-self.left)]

    def prefix(self, times, coverage=False):
        times = np.asarray(times, float)
        i = np.searchsorted(self.right, times, side='right')
        base = self.support[i] if coverage else self.area[i]
        if not len(self.left): return base
        j = np.minimum(i, len(self.left)-1)
        dt = np.clip(times-self.left[j], 0, self.right[j]-self.left[j])
        partial = dt if coverage else (self.a[j]*dt + .5*(self.b[j]-self.a[j])*dt**2/(self.right[j]-self.left[j]))/3600
        return base + np.where(i < len(self.left), partial, 0)

    def integral(self, start, end):
        return float(self.prefix(end)-self.prefix(start)) / 1000

    def coverage(self, start, end):
        return float(self.prefix(end, True)-self.prefix(start, True))/(end-start)*100 if end > start else 0.

    def sample(self, time):
        if len(self.t):
            k = np.searchsorted(self.t, time)
            if k < len(self.t) and self.t[k] == time:
                return float(self.v[k]), 'MEASURED'
        i = np.searchsorted(self.left, time, side='right')-1
        if i < 0 or time > self.right[i]: return None, 'UNAVAILABLE'
        return float(self.a[i]+(self.b[i]-self.a[i])*(time-self.left[i])/(self.right[i]-self.left[i])), 'SHORT_GAP_INTERPOLATED'

    def save(self, path):
        np.savez_compressed(path, t=self.t, v=self.v, left=self.left, right=self.right, a=self.a, b=self.b)

    @classmethod
    def load(cls, path):
        with np.load(path) as f:
            obj = cls.segments(f['left'], f['right'], f['a'], f['b'])
            obj.t, obj.v = f['t'], f['v']
        return obj


def combine(sensors):
    """Equal sensor mean on overlaps; single sensor elsewhere. Never sum detector doses."""
    knots = np.unique(np.concatenate([np.r_[s.left, s.right] for s in sensors]))
    left, right = knots[:-1], knots[1:]
    mid = (left+right)/2
    av, bv, count = np.zeros(len(mid)), np.zeros(len(mid)), np.zeros(len(mid))
    for s in sensors:
        i = np.searchsorted(s.left, mid, side='right')-1
        j = np.clip(i, 0, len(s.left)-1)
        valid = (i >= 0) & (mid <= s.right[j])
        slope = (s.b[j]-s.a[j])/(s.right[j]-s.left[j])
        av += np.where(valid, s.a[j]+slope*(left-s.left[j]), 0)
        bv += np.where(valid, s.a[j]+slope*(right-s.left[j]), 0)
        count += valid
    valid = count > 0
    return Stream.segments(left[valid], right[valid], av[valid]/count[valid], bv[valid]/count[valid])

