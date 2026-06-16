import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ising import run_simulation, create_animation, error_args, save_magnetization, plot_magnetization, plot_energy


#The argparse module’s support for command-line interfaces is built around an instance of argparse.ArgumentParser. 
#parser = argparse.ArgumentParser(prog='ProgramName',description='What the program does',epilog='Text at the bottom of help')

parser = argparse.ArgumentParser(description='Run the Ising model simulation.')
parser.add_argument('--N', type=int, default=100, help='Size of the lattice (default: 100)')
parser.add_argument('--J', type=float, default=1.0, help='Coupling constant (default: 1.0)')
parser.add_argument('--B', type=float, default=0.0, help='External magnetic field (default: 0.0)')
parser.add_argument('--beta', type=float, default=0.4, help='Inverse temperature (default: 0.4)')
parser.add_argument('--M', type=int, default=500, help='Number of Monte Carlo steps (default: 500)')
parser.add_argument('--save_magnetization', type=str, default=None, help='Filename to save magnetization data (default: None)')
parser.add_argument('--show_animation', action='store_true', help='Show animation of the simulation (default: False)')
parser.add_argument('--animation_file', type=str, default=None, help='Filename to save animation (default: None)')
args = parser.parse_args()

try:

    error_args(args)

    magnetyzacja, energie, frames = run_simulation(
        N=args.N,
        J=args.J,
        B=args.B,
        beta=args.beta,
        M=args.M
    )

    #args.save_magnetization = 15 DO TYPERROR 

    if args.save_magnetization is not None:

        if not isinstance(args.save_magnetization,str):
            raise TypeError("save_magnetization must be a string, zmien to asap !!!.")
        save_magnetization(
            args.save_magnetization,
            magnetyzacja
        )
        print(f"Magnetization data saved to {args.save_magnetization}")
    if args.animation_file is not None or args.show_animation:
        ani = create_animation(frames)
        if args.animation_file is not None:
            if args.animation_file.endswith(".gif"):
                ani.save(args.animation_file,writer="pillow")
            elif args.animation_file.endswith(".mp4"):
                ani.save(args.animation_file,writer="ffmpeg")
            else:
                raise ValueError("Use .gif or .mp4")
            print(f"Animation saved to {args.animation_file}")
        if args.show_animation:
            plt.show()

    print("N:", args.N)
    print("J:", args.J)
    print("B:", args.B)
    print("beta:", args.beta)
    print("M:", args.M)

    plot_magnetization(magnetyzacja)
    plot_energy(energie)
    plt.show()

except ValueError as e:
    print("Value Error oops:", e)

except TypeError as błąd:
    print( "TypeError oops:", błąd)

except Exception as e:
    print( "Unexpected error oops:", e)