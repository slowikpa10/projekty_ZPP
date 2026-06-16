
#Z numba 
@nb.njit
def sum_neighbors(spins, i, j):
    N = spins.shape[0]

    up = (i - 1) % N
    down = (i + 1) % N
    left = (j - 1) % N
    right = (j + 1) % N

    suma = (
        spins[up, j] +
        spins[down, j] +
        spins[i, left] +
        spins[i, right] +
        spins[up, left] +
        spins[up, right] +
        spins[down, left] +
        spins[down, right]
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
    return np.random.choice(np.array([-1, 1]), size=(N, N))


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

    energia = energia / 2.0
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

N = 50
J = 1.0
B = 0.0
beta = 0.4
M = 100 
magnetyzacja, energie, frames = run_simulation(N, J, B, beta, M)
fig, ax = plt.subplots()
im = ax.imshow(frames[0], vmin=-1, vmax=1)
ax.set_title("Model Isinga 2D")

def update(k):
    im.set_data(frames[k])
    ax.set_title(f"Makrokrok {k}")
    return [im]

anim = FuncAnimation(fig, update, frames=len(frames), interval=100, blit=True)
HTML(anim.to_jshtml())

#BEZ NUMBA 
def sum_neighbors_no_numba(spins, i, j): #licze sasiadow punktu i,j
    N = spins.shape[0]

    up = (i - 1) % N
    down = (i + 1) % N
    left = (j - 1) % N
    right = (j + 1) % N

    suma = (
        spins[up, j] +
        spins[down, j] +
        spins[i, left] +
        spins[i, right] +
        spins[up, left] +
        spins[up, right] +
        spins[down, left] +
        spins[down, right]
    )
    return suma

def delta_energy_no_numba(spins, i, j,J,B):
    s = spins[i, j]
    suma_sasiadow = sum_neighbors_no_numba(spins, i, j)
    return 2 * s * (J * suma_sasiadow + B)

def monte_carlo_step_no_numba(spins, J, B, beta): #definuje funkcje wykonujaca jeden krok symulacji Monte Carlo
    N = spins.shape[0] #losuje losowy indeks i,j w siatce

    i = np.random.randint(0, N)
    j = np.random.randint(0, N)

    dE = delta_energy_no_numba(spins, i, j, J, B)

    if dE <= 0:
        spins[i, j] = -spins[i, j]
    else:
        mniejsze_od_energii = np.random.random() #losuje liczbe z przedzialu [0,1), bo np.exp(-beta * dE) jest zawsze mniejsze od 1, wiec jesli wylosowana liczba jest mniejsza od tej wartosci, to odwracam spin
        if mniejsze_od_energii < np.exp(-beta * dE):
            spins[i, j] = -spins[i, j]
    
def monte_carlo_simulation_no_numba(spins, J, B, beta): #definiuje funkcje wykonujaca jeden makrokrok symulacji Monte Carlo, czyli N*N krokow
    N = spins.shape[0]
    for _ in range(N * N):
        monte_carlo_step_no_numba(spins, J, B, beta)

def oblicz_energie_no_numba(spins, J, B):
    N = spins.shape[0]
    energia = 0.0
    for i in range(N):
        for j in range(N):
            s = spins[i, j]
            suma_sasiadow = sum_neighbors_no_numba(spins, i, j)
            energia += -J * s * suma_sasiadow 
    energia = energia / 2.0
    energia += -B * np.sum(spins)
    return energia

def run_simulation_no_numba(N, J, B, beta, M):
    spins = poczatkowy_uklad_spinow(N) #funkcja generujaca poczatkowy uklad spinow, np losowy lub uporzadkowany
    magnetyzacja = []
    energie = []
    frames = []

    for _ in range(M):
        monte_carlo_simulation_no_numba(spins, J, B, beta) #wykonuje jeden makrokrok symulacji Monte Carlo, czyli N*N krokow
        magnetyzacja.append(oblicz_magnetyzacje(spins)) #oblicza magnetyzacje jako sume wszystkich spinow w siatce i zapisuje do listy
        energie.append(oblicz_energie_no_numba(spins, J, B)) #oblicza energie ukladu i zapisuje do listy
        frames.append(spins.copy()) #zapisuje aktualny uklad spinow do listy frames, zeby potem moc stworzyc animacje
    return magnetyzacja, energie, frames

N = 50
J = 1.0
B = 0.0
beta = 0.4
M = 100 

#czasy wykonania symulacji z numba i bez numba
import time
start_time = time.time()
magnetyzacja_no_numba, energie_no_numba, frames_no_numba = run_simulation_no_numba(N, J, B, beta, M)
end_time_numba = time.time() - start_time
print(f"Czas wykonania symulacji bez numba: {end_time_numba:.2f} sekund")

spins_test = poczatkowy_uklad_spinow(10)
monte_carlo_simulation(spins_test, J, B, beta)
start_time = time.time()
magnetyzacja_numba, energie_numba, frames_numba = run_simulation(N, J, B, beta, M)
czas_numba = time.time() - start_time

print(f"Czas z Numba: {czas_numba:.2f} s")

print(f"Przyspieszenie: {end_time_numba / czas_numba:.2f}x")

plt.subplot(1,2,1)
plt.plot(magnetyzacja_numba)
plt.title("Magnetyzacja")
plt.xlabel("Makrokrok")

plt.subplot(1,2,2)
plt.plot(energie_numba)
plt.title("Energia")
plt.xlabel("Makrokrok")

plt.tight_layout()
plt.show()
