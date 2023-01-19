import csv
import sys
import time
from inspect import Parameter
from environment import Environment
from q_learning import Q_Learning
from utils import runSmv, writeSmv
import numpy as np
import matplotlib.pyplot as plt
import parameters_run


# need to change size only on envioremnt, and utils (if used)

def main(p, learning_rate, index, discount_factor):
    # currently you can check 2 sizes an build graph for both together
    size1 = 10
    size2 = 20
    with_nuxmv = []
    without_nuxmv = []
    X = ['Converged ,with NuXmv', 'Did not converged ,with NuXmv', 'Converged ,without NuXmv',
         'Did not converged,without NuXmv']
    size10 = [0, 0, 0, 0]
    size20 = [0, 0, 0, 0]
    DictResults = {}
    DictResults["Converged ,with NuXmv"] = 0
    DictResults["Did not converged ,with NuXmv"] = 0
    DictResults["Converged ,without NuXmv"] = 0
    DictResults["Did not converged,without NuXmv"] = 0
    num_games = 50
    switch = int(num_games)  # switch between with and without nuxmv

    results = open("./results.csv", 'a')
    writer = csv.writer(results)
    writer.writerow(["size", "p", "learning_rate", "discount_factor", "with_nuxmv", "without_nuxmv"])

    for s in range(2):
        if s == 0:
            parameters_run.set_size(size1)

        if s == 1:
            parameters_run.set_size(size2)
        for i in range(num_games):
            frozen_lake_environment = Environment()
            q_learning_algo = Q_Learning(frozen_lake_environment, learning_rate, discount_factor)
            if i < switch:
                q_learning_algo.setuseNusmv(1)
            if i >= switch:
                q_learning_algo.setuseNusmv(0)

            q_learning_algo.run_algorithm(p, index)

            Q = q_learning_algo.getQ()
            H = frozen_lake_environment.get_holes()

            # q_learning_algo.print_results()
            success, e = q_learning_algo.run_and_print_latest_iteration(p)
            if success == 0 and i >= switch:
                if s == 0:
                    size10[3] += 1
                if s == 1:
                    size20[3] += 1
                without_nuxmv.append(e)

            if success == 0 and i < switch:
                if s == 0:
                    size10[1] += 1
                if s == 1:
                    size20[1] += 1
                with_nuxmv.append(e)
            if success == 1 and i >= switch:
                if s == 0:
                    size10[2] += 1
                if s == 1:
                    size20[2] += 1
                without_nuxmv.append(e)
            if success == 1 and i < switch:
                if s == 0:
                    size10[0] += 1
                if s == 1:
                    size20[0] += 1
                with_nuxmv.append(e)
        if s == 0:
            writer.writerow([parameters_run.get_size(), p, learning_rate, discount_factor, size10[0], size10[2]])
        if s == 1:
            writer.writerow([parameters_run.get_size(), p, learning_rate, discount_factor, size20[0], size20[2]])
    results.close()

    print("with nuxmv:", with_nuxmv)
    print("without nuxmv:", without_nuxmv)

    X_axis = np.arange(len(X))
    str1 = str(size1) + "x" + str(size1)
    str2 = str(size2) + "x" + str(size2)
    plt.bar(X_axis - 0.1, size10, 0.1, label=str1)
    plt.bar(X_axis + 0.1, size20, 0.1, label=str2)

    plt.xticks(X_axis, X)
    plt.ylim(0, max(size10) + 4)
    plt.ylabel("Number of games")
    plt.title(str(num_games) + " games of frozen lake for boards: " + str1 + " " + str2)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    prob = sys.argv[1]
    discount_rate = 0.92
    alpha = 0.2  # learning rate
    index = sys.argv[2]
    main(float(prob), float(alpha), index, discount_factor=discount_rate)
    print(float(prob))
    print("time:" + str(time.time() - start_time))
