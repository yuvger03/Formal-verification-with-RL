import sys

from parameters_run import ParametersRun
from environment import Environment
from q_learning import Q_Learning


# import matplotlib.pyplot as plt


def main(p, size, index):
    parameters_run = ParametersRun()
    parameters_run.setNewParameters(size)
    # DictResults = {}
    # DictResults["Converged ,with NuXmv"] = 0
    # DictResults["Did not converged ,with NuXmv"] = 0
    # DictResults["Converged ,without NuXmv"] = 0
    # DictResults["Did not converged,without NuXmv"] = 0
    num_games = 1
    switch = 2
    for i in range(num_games):
        get_the_cheese = Environment(parameters_run)
        q_learning_algo = Q_Learning(get_the_cheese, probability=p, index=index, PR=parameters_run)
        if i < switch:
            q_learning_algo.setuseNusmv(1)
        if i >= switch:
            q_learning_algo.setuseNusmv(0)

        q_learning_algo.run_algorithm(index)

        Q = q_learning_algo.getQ()
        H = get_the_cheese.get_holes()

        q_learning_algo.print_results()
        r = q_learning_algo.run_and_print_latest_iteration()
        if r == 0 and i >= switch:
            # DictResults["Did not converged,without NuXmv"] += 1
            print("Did not converged,without NuXmv")
        if r == 0 and i < switch:
            # DictResults["Did not converged ,with NuXmv"] += 1
            print("Did not converged ,with NuXmv")
        if r == 1 and i >= switch:
            # DictResults["Converged ,without NuXmv"] += 1
            print("Converged ,without NuXmv")
        if r == 1 and i < switch:  # to change
            # DictResults["Converged ,with NuXmv"] += 1
            print("Converged ,with NuXmv")
        print(q_learning_algo.q_table)
    # width = 0.1
    # plt.bar(DictResults.keys(), DictResults.values(), width)
    # plt.ylabel('Games')
    #
    # # displaying the title
    # plt.title(str(num_games) + " games of Catch the cheese")
    # plt.show()
    # plt.savefig(f'tests/graph{p}.png')


if __name__ == '__main__':
    # for size in [10,15,20]:
    #     for j in range(0,9):
    #         p = 1 - j * 0.05
    main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
