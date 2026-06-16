
import numpy as np
import numba as nb


@nb.njit
def sum_neighbors(spins, i, j):

    N = spins.shape[0]

    up = (i - 1) % N
    down = (i + 1) % N
    left = (j - 1) % N
    right = (j + 1) % N

    suma = (
        spins[up, j]
        + spins[down, j]
        + spins[i, left]
        + spins[i, right]
        + spins[up, left]
        + spins[up, right]
        + spins[down, left]
        + spins[down, right]
    )

    return suma


@nb.njit
def delta_energy(spins, i, j, J, B):

    s = spins[i, j]

    suma_sasiadow = sum_neighbors(spins, i, j)

    return 2 * s * (J * suma_sasiadow + B)


@nb.njit
def monte_carlo_step(spins, J, B, beta):

    N = spins.shape[0]

    i = np.random.randint(0, N)
    j = np.random.randint(0, N)

    dE = delta_energy(spins, i, j, J, B)

    if dE <= 0:

        spins[i, j] = -spins[i, j]

    else:

        if np.random.random() < np.exp(-beta * dE):

            spins[i, j] = -spins[i, j]


@nb.njit
def monte_carlo_simulation(spins, J, B, beta):

    N = spins.shape[0]

    for _ in range(N * N):

        monte_carlo_step(spins, J, B, beta)


def poczatkowy_uklad_spinow(N):

    return np.random.choice(
        np.array([-1, 1]),
        size=(N, N)
    )


def oblicz_magnetyzacje(spins):

    return np.sum(spins) / (spins.shape[0] ** 2)


@nb.njit
def oblicz_energie(spins, J, B):

    N = spins.shape[0]

    energia = 0.0

    for i in range(N):

        for j in range(N):

            s = spins[i, j]

            suma_sasiadow = sum_neighbors(spins, i, j)

            energia += -J * s * suma_sasiadow

    energia /= 2.0

    energia += -B * np.sum(spins)

    return energia


def run_simulation(N, J, B, beta, M):

    spins = poczatkowy_uklad_spinow(N)

    magnetyzacja = []
    energie = []
    frames = []

    for _ in range(M):

        monte_carlo_simulation(spins, J, B, beta)

        magnetyzacja.append(oblicz_magnetyzacje(spins))
        energie.append(oblicz_energie(spins, J, B))
        frames.append(spins.copy())

    return magnetyzacja, energie, frames

