
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

def create_animation(frames):
    fig, ax = plt.subplots()

    img = ax.imshow(frames[0], cmap="gray", animated=True)
    ax.set_title("Model Isinga")

    def update(frame):
        img.set_array(frame)
        return [img]

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=100,
        blit=True
    )

    return ani
def plot_magnetization(magnetyzacja):
    plt.figure()
    plt.plot(magnetyzacja)
    plt.xlabel("Makrokrok")
    plt.ylabel("Magnetyzacja")
    plt.title("Magnetyzacja w funkcji czasu")
    plt.grid()
    

def plot_energy(energie):
    plt.figure()
    plt.plot(energie)
    plt.xlabel("Makrokrok")
    plt.ylabel("Energia")
    plt.title( "Energia w funkcji czasu")
    plt.grid()
    