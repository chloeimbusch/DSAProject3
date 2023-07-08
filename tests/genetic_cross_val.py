import itertools
import time

from random_city import RandomCity

# Allow import from src folder
from sys import path
from os.path import dirname
path.append(dirname(path[0]))
from src.approximations.genetic_approximation import GeneticApproximation
from src.functions import calc_fitness_memo


class GeneticCrossVal:
    def __init__(self, population: list, param_grid: dict) -> dict:
        self.population = population
        self.param_grid = param_grid

    def fit(self) -> list[tuple[dict, float, float, float]]:
        """Performs grid search cross validation on the provided paramater grid

        Returns:
            list: List containing tuples of the paramater set, fitness score, the distance of the last run (1 / fitness score), and duration of the test cycle for that paramater set
        """

        param_scores = []

        # Perform grid search cross val over all combinations of params
        for params in itertools.product(*self.param_grid.values()):
            run_scores = []
            final_avg_dist = 0

            # Repeat 5 times to get average and account for randomness
            start = time.time()
            for _ in range(5):
                gen_approx = GeneticApproximation(self.population, *params)
                done = False
                while not done:
                    best, done = gen_approx.run()
                    run_scores.append(best)
                final_avg_dist += 1 / run_scores[-1]
            
            duration = time.time() - start

            param_scores.append((params, sum(run_scores), final_avg_dist / 5, duration))

        return sorted(param_scores, key = lambda x: x[1], reverse = True)
            

if __name__ == "__main__":
    num_cities = 100
    map_size = 200
    city_list = [RandomCity(map_size) for _ in range(num_cities)]

    params = {'pop_size': [100, 150, 200, 250], 'elite_size': [10, 20, 30, 40], 'mutation_rate': [0.0001, 0.001, 0.01, 0.1], 'num_generations': [250, 500]}
    genetic_cv = GeneticCrossVal(city_list, params)
    param_scores = genetic_cv.fit()
    print(param_scores[:25])


# Results: 19 Jun, 25 cities
# params = {'pop_size': [50, 100, 150, 200, 250], 'elite_size': [10, 20, 30, 40, 50], 'mutation_rate': [0.001, 0.01, 0.1, 0.2, 0.5], 'num_generations': [250]}
"""[((250, 10, 0.001, 250), 1.2758261618221556, 69.74723291397095),
   ((200, 40, 0.001, 250), 1.272967583052799, 45.812567949295044),
   ((250, 20, 0.001, 250), 1.267630644322337, 68.94131994247437),
   ((250, 30, 0.001, 250), 1.2629407809680888, 66.27685284614563),
   ((200, 20, 0.001, 250), 1.2534909655376318, 49.896891832351685),
   ((250, 40, 0.001, 250), 1.2520705225555897, 64.45660543441772),
   ((200, 10, 0.001, 250), 1.2488410738703255, 52.04733395576477),
   ((200, 30, 0.001, 250), 1.2460389083180676, 47.402432441711426),
   ((200, 50, 0.001, 250), 1.2459801423370476, 43.983081340789795),
   ((150, 40, 0.001, 250), 1.2320677729675493, 30.32062578201294),
   ((250, 10, 0.01, 250), 1.228139715864845, 71.1129162311554),
   ((100, 10, 0.001, 250), 1.2275070213526698, 19.540728330612183),
   ((100, 30, 0.001, 250), 1.2234200830809803, 16.682739973068237),
   ((150, 10, 0.001, 250), 1.2225501319403524, 34.2347252368927),
   ((250, 20, 0.01, 250), 1.2179754585612779, 69.14761781692505),
   ((250, 30, 0.01, 250), 1.217845157411731, 66.25005531311035),
   ((250, 40, 0.01, 250), 1.2143402028450498, 63.4615523815155),
   ((150, 50, 0.001, 250), 1.2122591036942596, 28.029962301254272),
   ((250, 50, 0.001, 250), 1.2087984121010844, 61.70221996307373),
   ((200, 40, 0.01, 250), 1.2070118375553733, 44.761268615722656)]"""

# Results: 20 Jun, 100 cities
# params = {'pop_size': [100, 150, 200, 250], 'elite_size': [10, 20, 30, 40], 'mutation_rate': [0.001, 0.01, 0.1], 'num_generations': [250]}
"""[((200, 10, 0.001, 250), 0.3803472059183128, 2483.458453133819, 84.43745112419128),
    ((250, 10, 0.001, 250), 0.3776175413560789, 2761.3721447161506, 111.8234543800354),
    ((250, 20, 0.001, 250), 0.3776055812328988, 2535.914036835535, 109.12084794044495),
    ((250, 30, 0.001, 250), 0.3696472232965492, 2563.5081072170933, 111.50230884552002),
    ((250, 40, 0.001, 250), 0.36359525908418566, 3173.6595639133025, 104.3448965549469),
    ((150, 10, 0.001, 250), 0.3629867660366671, 2710.1895750781314, 62.385509967803955),
    ((200, 30, 0.001, 250), 0.3569411375609765, 3207.651875399626, 80.04993033409119),
    ((200, 20, 0.001, 250), 0.3539459063171421, 2755.99391464468, 82.2824273109436),
    ((200, 40, 0.001, 250), 0.35290360910596086, 2660.8759366499753, 77.4909839630127),
    ((150, 20, 0.001, 250), 0.3447032115064268, 3121.439647328029, 59.37563157081604),
    ((150, 30, 0.001, 250), 0.3385261330853166, 2900.151206449551, 57.81723952293396),
    ((150, 40, 0.001, 250), 0.3269917628578514, 2982.0797776490936, 52.925923347473145),
    ((100, 10, 0.001, 250), 0.32446897308222067, 2820.485959513064, 37.29929184913635),
    ((100, 20, 0.001, 250), 0.3130546944241745, 3099.1427725783383, 36.303224325180054),
    ((100, 30, 0.001, 250), 0.3007234495911202, 3715.0100517814885, 34.364166498184204),
    ((100, 40, 0.001, 250), 0.2795785825093939, 3564.3674021646275, 32.335949420928955),
    ((250, 20, 0.01, 250), 0.26515751179186076, 3953.982458074785, 115.09479832649231),
    ((250, 10, 0.01, 250), 0.2599528839932267, 3789.1574984313634, 111.1136691570282),
    ((200, 20, 0.01, 250), 0.25833839038660095, 4276.047672527054, 81.7923276424408),
    ((250, 30, 0.01, 250), 0.25778178372080957, 3895.1883374824574, 109.15412831306458),
    ((250, 40, 0.01, 250), 0.2568766934624212, 4300.808973795859, 103.46301531791687),
    ((200, 10, 0.01, 250), 0.25371721801917746, 4345.058107531797, 83.81487154960632),
    ((200, 30, 0.01, 250), 0.24863786174191413, 4818.013930605051, 80.84178066253662),
    ((150, 10, 0.01, 250), 0.24484293608737415, 4555.184479271291, 61.67592406272888),
    ((150, 20, 0.01, 250), 0.23726064558072224, 4491.163317531129, 59.1850061416626)]"""

# Results: 20 Jun, 100 cities
# params = {'pop_size': [100, 150, 200, 250], 'elite_size': [10, 20, 30, 40], 'mutation_rate': [0.0001, 0.001, 0.01, 0.1], 'num_generations': [250, 500]}
"""[((200, 20, 0.0001, 500), 0.871430956935287, 2381.03269414095, 164.64229345321655),
((250, 10, 0.001, 500), 0.8635361872031518, 2527.115900709614, 225.08441472053528),
((250, 30, 0.0001, 500), 0.861868975951369, 2475.2767851334584, 220.0873806476593),
((250, 10, 0.0001, 500), 0.8612217235136264, 2476.2648411977843, 225.93795156478882),
((250, 20, 0.0001, 500), 0.8461952994939737, 2491.756298715688, 213.31302046775818),
((200, 10, 0.001, 500), 0.8455570897553755, 2456.0189813569477, 173.58990573883057),
((250, 30, 0.001, 500), 0.839718620806309, 2459.3810049159883, 218.20135617256165),
((250, 40, 0.0001, 500), 0.8171947923290309, 2652.947218678427, 215.11519026756287),
((250, 40, 0.001, 500), 0.8161718817583516, 2528.6101018160057, 214.92002749443054),
((150, 10, 0.001, 500), 0.8028279343053465, 2642.6966790518827, 124.56063961982727),
((250, 20, 0.001, 500), 0.8009843924279969, 2659.8339990007203, 212.4810471534729),
((200, 20, 0.001, 500), 0.7981233043152204, 2664.963410839469, 169.4201467037201),
((200, 10, 0.0001, 500), 0.7973764991546138, 2550.887527441572, 183.72711181640625),
((200, 40, 0.001, 500), 0.7918454434710226, 2603.1003884286197, 154.61815333366394),
((150, 20, 0.001, 500), 0.7732927225544329, 2653.5247857292156, 115.29095315933228),
((200, 40, 0.0001, 500), 0.7726333985104725, 2782.6098820285524, 155.09108638763428),
((200, 30, 0.0001, 500), 0.7697054370280829, 2870.9632033910393, 160.03634405136108),
((150, 20, 0.0001, 500), 0.7663878548619015, 2803.90228095034, 115.527259349823),
((150, 10, 0.0001, 500), 0.7527618751548382, 2886.6486150739292, 123.49448823928833),
((150, 30, 0.0001, 500), 0.7477169010322192, 2903.7326739832947, 115.26598310470581),
((100, 10, 0.001, 500), 0.7454170949977174, 2784.715074772852, 71.8396246433258),
((200, 30, 0.001, 500), 0.7404135272122366, 2952.2528609214614, 160.35721826553345),
((150, 40, 0.0001, 500), 0.7355496610805435, 2852.9795295504446, 108.6758348941803),
((150, 40, 0.001, 500), 0.7322000347636364, 2765.44243410122, 111.63524866104126),
((150, 30, 0.001, 500), 0.7311195051106373, 2929.62998615975, 114.12013912200928)]"""