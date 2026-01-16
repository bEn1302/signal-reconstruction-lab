import numpy as np
from scipy.interpolate import interp1d


"""
Abtastung: Nimmt nur jeden n-ten Wert aus ganz x
doc: https://stackoverflow.com/questions/509211/how-slicing-in-python-works
"""


def downsample_signal(x, t, factor):
    x_sampled = x[::factor]
    t_sampled = t[::factor]
    return x_sampled, t_sampled


"""
Rekonstruiert das Signal auf drei verschiedene Arten
doc: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d
"""


def reconstruct_signal(t_sampled, x_sampled, t_original):
    results = {}

    # 1. Stufenform
    f_step = interp1d(t_sampled, x_sampled, kind="previous", fill_value="extrapolate")
    results["stufen"] = f_step(t_original)

    # 2. Linearisierung
    f_linear = interp1d(t_sampled, x_sampled, kind="linear", fill_value="extrapolate")
    results["linear"] = f_linear(t_original)

    # 3. Kubische Approximation
    f_cubic = interp1d(t_sampled, x_sampled, kind="cubic", fill_value="extrapolate")
    results["kubisch"] = f_cubic(t_original)

    # 4. (Lagrange-Interpolation über ganzes Signal ist mathematisch instabil & rechenintensiv)

    return results
