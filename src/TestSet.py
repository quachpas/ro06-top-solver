
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
import pandas as pd


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
    best_solution: float

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + "name=%s, " % self.name
            + "N=%d, " % self.N
            + "m=%d, " % self.m
            + "tmax=%.2f, " % self.tmax
            + "best_solution=%.2f, " % self.best_solution
            + "P=..., C=...)"
        )


def read_test_sets(dirpath: Path, filepath: Path):
    test_sets = glob(str(dirpath / "Set*"))
    test_dict = {}
    best_solutions = read_best_solutions(filepath)
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
        name = Path(filename).stem
        test_dict[test_set] += [
            TestInstance(
                name=name,
                N=N,
                m=m,
                tmax=tmax,
                P=P,
                C=C,
                X=X,
                best_solution=best_solutions[name]
                if name in best_solutions
                else np.nan,
            )
        ]

    return test_dict


def read_best_solutions(filepath: Path):
    df = pd.read_csv(filepath).set_index("name").astype(float)
    return df.to_dict()["solution"]


def read_Chao(
    dpath: Path = Path("../ro06-projet-a22/Chao/"),
    fpath: Path = Path("../src/best_solutions_kim_et_al_2013.csv"),
):
    if not dpath.exists() or not fpath.exists():
        raise FileNotFoundError
    return read_test_sets(dpath, fpath)


def read_Tsiligirides(
    dpath: Path = Path("../ro06-projet-a22/Tsiligirides/"),
    fpath: Path = Path("../src/best_solutions_kim_et_al_2013.csv"),
):
    if not dpath.exists() or not fpath.exists():
        raise FileNotFoundError
    return read_test_sets(dpath, fpath)

