import csv
import os


def RW(size):
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


for i in [ 1000]:
    resfile = open(f"resCTC{i}.csv", 'a', newline='')

    writer = csv.writer(resfile)
    fileStart = r"tests/nuxmv_prism_results_"
    # for size in [10]:
    #     for j in range(0, 19):
    #         p = 1 - j * 0.05
    #         file = fileStart + str(size) + str(p) + ".csv"
    entries = os.listdir(f'tests/{i},5/')
    os.chdir(f'tests/{i},5/')
    for size in [10, 15, 20, 25, 30, 40]:
        RW(size)
    resfile.close()
