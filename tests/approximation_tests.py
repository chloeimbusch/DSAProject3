import matplotlib.pyplot as plt
import time

from random_city import RandomCity

# Allow import from src folder
from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from src.approximations.genetic_approximation import GeneticApproximation
from src.approximations.nearest_neighbor import NearestNeighbor
from src.approximations.simulated_annealing import SimmulatedAnnealing
from src.approximations.particle_swarm_optimization import ParticleSwarmOptimization
from src.approximations.ant_colony_opimization import AntColonyOptimization
from src.approximations.greedyheuristic import Greedy
from src.approximations.greedy_2opt import GreedyTwoOpt

if __name__ == '__main__':
    # Counteracts the matplotlib.use('Agg') in run_state which allows drawing to pygame surface
    import matplotlib
    matplotlib.use('tkagg')

    num_cities = 200
    map_size = 200
    city_list = [RandomCity(map_size) for _ in range(num_cities)]

    approximations = [Greedy, GreedyTwoOpt]
    names = []
    plt.figure(figsize=(20, 12), dpi=80)
    for approx in approximations:
        approx = approx(city_list)
        names.append(approx.__class__.__name__)
        start = time.time()
        done = False
        scores = []
        while not done:
            best, done = approx.run()
            scores.append(1 / best)

        print(f'{names[-1]}: {str(time.time() - start)}')
        plt.plot(scores)

    plt.ylabel('Distance')
    plt.xlabel('Iteration') 
    plt.xscale('log')
    plt.legend(names)
    plt.show()
