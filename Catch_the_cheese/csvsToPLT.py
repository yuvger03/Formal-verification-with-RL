import csv
import os
import matplotlib.pyplot as plt


def writeData(folder, res_file):
    for i in [1000]:
        entries = os.listdir(folder)
        os.chdir(folder)

        resfile = open(res_fil, 'a', newline='')
        writer = csv.writer(resfile)
        fileStart = fr"{folder}/nuxmv_prism_results_"
        # for size in [10]:
        #     for j in range(0, 19):
        #         p = 1 - j * 0.05
        #         file = fileStart + str(size) + str(p) + ".csv"
        for size in [10, 15, 20, 25, 30, 40]:
            RW(size, entries, writer)
        resfile.close()
    # os.chdir("..")


def RW(size, entries, writer):
    for entry in entries:
        print(entry)
        if entry.endswith(".csv") and entry.startswith("nuxmv_prism_results_" + str(size)):
            print(entry)
            with open(entry, 'r', newline='') as csvfile:  # read the ladt line of the csv file
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    pass
                lastrow = row
                writer.writerow([size, 0, lastrow[0]])


def csvPlot(filename):
    probs = [float(p / 100) for p in range(0, 105, 5)]
    data_size = {10: [], 15: [], 20: [], 25: [], 30: [], 40: []}
    with open(filename, 'r', newline='') as csvfile:
        currentSize = 10
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if int(row[0]) != currentSize:
                currentSize = int(row[0])
            if 'Error' in row[2]:
                data_size[currentSize].append(None)
            else:
                data_size[currentSize].append(float(row[2]))

    for s in [10, 15, 20, 25, 30, 40]:
        plt.plot(probs, data_size[s], '-o', label=str(s))
    plt.legend(title="Size")
    plt.xlabel("p")
    plt.ylabel("Probability of losing")
    plt.title(f"Probability of losing vs p")  #  using {filename[6:-4]} iterations
    plt.savefig(filename[:-4] + ".png")
    plt.show()


# csvPlot("resCTCNewfolder.csv")
file_name = "resCTCTest.csv"
writeData("./results", file_name)
# print(os.path.abspath("./resCTCNewFolder.csv"))
csvPlot(f"./{file_name}")

