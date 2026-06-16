from .simulation import run_simulation
from .visualization import (create_animation,plot_magnetization, plot_energy)
from .io_utils import save_magnetization, error_args
#pozwala nam dawać bezpośrednio z importować funkcje z tych modułów, np. from ising import run_simulation, create_animation
#nie musze pisac from ising.simulation import run_simulation

#Próby 
#python run_ising.py --N 50 --J 1.0 --B 0.0 --beta 0.4 --M 500 --save_magnetization magnetyzacja.txt --show_animation --animation_file animacja.gif
#python run_ising.py --animation_file animacja.gif
#python run_ising.py --show_animation 
#python run_ising.py --save_magnetization magnetyzacja.txt

#Dla ValuError: python run_ising.py --N -50
#Dla TypeError: python run_ising.py --save_magnetization 15