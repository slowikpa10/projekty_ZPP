def save_magnetization(filename, magnetyzacja):
    with open(filename, "w") as f:
        for step, value in enumerate(magnetyzacja):
            f.write(f"{step} {value}\n") 


def error_args(args):
    if args.N <= 0:
        raise ValueError("N must be a positive integer.")
    if args.M <= 0:
        raise ValueError("M must be a positive integer.")
    if args.beta <= 0:
        raise ValueError("beta must be a positive float.")