#!/usr/bin/env python
# coding: utf-8

__all__ = [
    "read_Chao",
    "read_Tsiligirides",
]
import pulp
import numpy as np
from glob import glob
from dataclasses import dataclass, field
from scipy.spatial import distance
from pathlib import Path

@dataclass
class TestInstance:
    """
    Params:
        name: name of the instance
        N: number of clients
        m: number of vehicles
        tmax: maximum allocated time per vehicle
        P: profit per client
        C: travel cost (time)
        X: original point data
    """
    name: str
    N: int
    m: int
    tmax: float
    P: np.ndarray
    C: np.ndarray
    X: np.ndarray
    
    def __repr__(self):
        return self.__class__.__name__ + "(" + "name=%s, " % self.name + "N=%d, " % self.N + "m=%d, " % self.m + "tmax=%.2f, " % self.tmax + "P=..., C=...)"

def read_test_sets(dirpath: Path):
    test_sets = glob(str(dirpath / "Set*"))
    test_dict = {}
    for filename in glob(str(dirpath / "Set*/*.txt")):
        test_set = Path(filename).parts[-2]
        with open(filename) as f:
            N = int(f.readline().split(" ")[-1])
            m = int(f.readline().split(" ")[-1])
            tmax = float(f.readline().split(" ")[-1])
            arr = np.loadtxt(f)
            X, P = np.split(arr, [2], axis=1)
            C = distance.squareform(distance.pdist(X))
        if test_set not in test_dict:
            test_dict[test_set] = []
        test_dict[test_set] += [TestInstance(
            name=Path(filename).stem,
            N=N,
            m=m,
            tmax=tmax,
            P=P,
            C=C,
            X=X
        )]
        
    return test_dict

def read_Chao():
    dpath = Path("../ro06-projet-a22/Chao/")
    if not dpath.exists():
        raise FileNotFoundError
    return read_test_sets(dpath)

def read_Tsiligirides():
    dpath = Path("../ro06-projet-a22/Tsiligirides/")
    if not dpath.exists():
        raise FileNotFoundError
    return read_test_sets(dpath)


if __name__ == "__main__":
    Chao = read_test_sets(Path("../ro06-projet-a22/Chao/"))
    print(Chao["Set_100_234"])

