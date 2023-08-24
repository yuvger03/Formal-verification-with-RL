import csv
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def writeData(folder, res_file, sizes):
    for i in [1000]:
        print(os.getcwd())
        entries = os.listdir(folder)
        os.chdir(folder)

        resfile = open(res_file, 'a', newline='')
        writer = csv.writer(resfile)
        fileStart = fr"{folder}/nuxmv_prism_results_"
        # for size in [10]:
        #     for j in range(0, 19):
        #         p = 1 - j * 0.05
        #         file = fileStart + str(size) + str(p) + ".csv"
        for size in sizes:
            RW(size, entries, writer)
        resfile.close()
    # os.chdir("..")


def RW(size, entries, writer):
    for entry in entries:
        print(entry)
        if entry.endswith(".csv") and entry.startswith("nuxmv_prism_results_" + str(size)):
            prob = entry.replace("nuxmv_prism_results_" + str(size), "").replace(".csv", "")
            with open(entry, 'r', newline='') as csvfile:  # read the ladt line of the csv file
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    pass
                lastrow = row
                writer.writerow([size, prob, lastrow[0]])
                print([size, prob, lastrow[0]])


def csvPlot(filename, sizes):
    probs = []
    data_size = {size: [] for size in sizes}
    with open(filename, 'r', newline='') as csvfile:
        currentSize = 10
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if int(row[0]) != currentSize:
                currentSize = int(row[0])
            if float(row[1]) not in probs:
                probs.append(float(row[1]))
            if 'Error' in row[2]:
                data_size[currentSize].append(None)
            else:
                data_size[currentSize].append(float(row[2]))

    figure(figsize=(15, 7))
    print(probs)
    for s in sizes:
        print(data_size[s])
        plt.plot(probs[len(probs)-1:len(probs)-11:-1], data_size[s][len(probs)-1:len(probs)-11:-1], '-o', label=str(s))

    plt.legend(title="Size")
    plt.xlabel("p")
    plt.ylabel("Probability of convergence")
    plt.xticks(probs[len(probs)-1:len(probs)-11:-1])
    plt.title(f"Probability of convergence vs p")  #  using {filename[6:-4]} iterations
    # save plot as pdf and png
    plt.savefig(filename[:-4] + ".pdf")
    plt.savefig(filename[:-4] + ".png")
    plt.show()


# csvPlot("resCTCNewfolder.csv")
def main(game='Frozen_lake'):
    os.chdir(r"C:\Users\liri\PycharmProjects\FV&RL")  # change to the main directory
    if game == 'Frozen_lake':
        sizes = [10, 20]
        file_name = "resFL.csv"
    else:  # CTC
        sizes = [10, 15, 20, 25, 30, 40]
        file_name = "resCTC.csv"

    writeData(f"./{game}/results", file_name, sizes)
    # print(os.path.abspath("./resCTCNewFolder.csv"))
    csvPlot(f"./{file_name}", sizes)


if __name__ == '__main__':
    main('Frozen_lake')
