# Credits to the authors of the work "Data-driven discovery of coordinates and governing equations":
# Kathleen Champion, Bethany Lusch, J. Nathan Kutz, Steven L. Brunton
# and "Machine Learning Methods for Nonlinear Reduced-order Modeling of the Thermospheric Density Field"
# Vahid Nateghi, Matteo Manzi

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.special import legendre

def get_lorenz_data(n_ics, noise_strength=0):
    """
    Generate a set of Lorenz training data for multiple random initial conditions.
    Arguments:
        n_ics - Integer specifying the number of initial conditions to use.
        noise_strength - Amount of noise to add to the data.
    Return:
        data - Dictionary containing elements of the dataset. See generate_lorenz_data()
        doc string for list of contents.
    """
    t = np.arange(0, 5, 0.02)
    input_dim = 128

    ic_means = np.array([0, 0, 25])
    ic_widths = 2 * np.array([36, 48, 41])

    # training data
    ics = ic_widths * (np.random.rand(n_ics, 3) - 0.5) + ic_means
    data, target = generate_lorenz_data(
        ics, t, input_dim, normalization=np.array([1 / 90, 1 / 90, 1 / 90])
    )
    data = data.reshape((-1,input_dim)) + noise_strength*np.random.randn(t.size*n_ics,input_dim)
    target = target.reshape((-1,))
    return data, target


def simulate_lorenz(z0, t, sigma=10.0, beta=8 / 3, rho=28.0):
    """
    Simulate the Lorenz dynamics.
    Arguments:
        z0 - Initial condition in the form of a 3-value list or array.
        t - Array of time points at which to simulate.
        sigma, beta, rho - Lorenz parameters
    Returns:
        z - Array of the trajectory values.
    """
    f = lambda z, t: [
        sigma * (z[1] - z[0]),
        z[0] * (rho - z[2]) - z[1],
        z[0] * z[1] - beta * z[2],
    ]
    z = odeint(f, z0, t)
    return z


def generate_lorenz_data(
    ics, t, n_points, normalization=None, sigma=10, beta=8 / 3, rho=28
):
    """
    Generate high-dimensional Lorenz data set.
    Arguments:
        ics - Nx3 array of N initial conditions
        t - array of time points over which to simulate
        n_points - size of the high-dimensional dataset created
        normalization - Optional 3-value array for rescaling the 3 Lorenz variables.
        sigma, beta, rho - Parameters of the Lorenz dynamics.
    Returns:
        data - Dictionary containing elements of the dataset. This includes the time points (t),
        spatial mapping (y_spatial), high-dimensional modes used to generate the full dataset
        (modes), low-dimensional Lorenz dynamics (z, along with 1st and 2nd derivatives dz and
        ddz), high-dimensional dataset (x, along with 1st and 2nd derivatives dx and ddx), and
        the true Lorenz coefficient matrix for SINDy.
    """
    n_ics = ics.shape[0]
    n_steps = t.size

    d = 3
    z = np.zeros((n_ics, n_steps, d))
    for i in range(n_ics):
        z[i] = simulate_lorenz(ics[i], t, sigma=sigma, beta=beta, rho=rho)

    if normalization is not None:
        z *= normalization

    n = n_points
    L = 1
    y_spatial = np.linspace(-L, L, n)
    modes = np.zeros((2 * d, n))
    for i in range(2 * d):
        test = legendre(i)
        modes[i] = legendre(i)(y_spatial)

    x1 = np.zeros((n_ics, n_steps, n))
    x2 = np.zeros((n_ics, n_steps, n))
    x3 = np.zeros((n_ics, n_steps, n))
    x4 = np.zeros((n_ics, n_steps, n))
    x5 = np.zeros((n_ics, n_steps, n))
    x6 = np.zeros((n_ics, n_steps, n))
    norm = np.zeros((n_ics, n_steps))


    x = np.zeros((n_ics, n_steps, n))
    for i in range(n_ics):
        for j in range(n_steps):
            x1[i, j] = modes[0] * z[i, j, 0]
            x2[i, j] = modes[1] * z[i, j, 1]
            x3[i, j] = modes[2] * z[i, j, 2]
            x4[i, j] = modes[3] * z[i, j, 0] ** 3
            x5[i, j] = modes[4] * z[i, j, 1] ** 3
            x6[i, j] = modes[5] * z[i, j, 2] ** 3
            norm[i, j] = np.linalg.norm(z[i, j, :])

            x[i, j] = (
                x1[i, j] + x2[i, j] + x3[i, j] + x4[i, j] + x5[i, j] + x6[i, j]
            )

    return x, norm

noise_strength = 1e-6
features, target = get_lorenz_data(1024, noise_strength=noise_strength)

import pandas as pd

df = pd.DataFrame(features)
df.columns = df.columns.astype(str)
df.to_parquet('features.parquet')

df = pd.DataFrame(target)
df.columns = df.columns.astype(str)
df.to_parquet('target.parquet')