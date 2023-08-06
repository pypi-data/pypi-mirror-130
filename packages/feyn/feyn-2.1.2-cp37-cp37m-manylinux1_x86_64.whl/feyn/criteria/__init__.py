import numpy as np

from ._structural import _sort_by_structural_diversity
from ._clustering import _assign_qcells_by_clustering
from ._bootstrap import _assign_qcells_by_bootstrap
from ._readability import _sort_by_readability
from ..tools import kind_to_output_stype

__all__ = [
    "bic",
    "aic",
    "aicc",
]


def bic(loss_value: float, param_count: int, n_samples: int, kind: str) -> float:
    out_type = kind_to_output_stype(kind)
    if out_type == "f":
        ans = n_samples * np.log(loss_value + 1e-7) + param_count * np.log(n_samples)
    elif out_type == "b":
        ans = n_samples * loss_value * 2 + param_count * np.log(n_samples)
    else:
        raise ValueError()

    return ans


def aic(loss_value: float, param_count: int, n_samples: int, kind: str) -> float:
    out_type = kind_to_output_stype(kind)
    if out_type == "f":
        ans = n_samples * np.log(loss_value + 1e-7) + param_count * 2
    elif out_type == "b":
        ans = n_samples * loss_value * 2 + param_count * 2
    else:
        raise ValueError()

    return ans


def aicc(loss_value: float, param_count: int, n_samples: int, kind: str) -> float:

    ans = aic(loss_value, param_count, n_samples, kind) + (
        2 * (param_count ** 2) + (2 * param_count)
    ) / (n_samples - param_count - 1 + 1e-7)

    return ans
