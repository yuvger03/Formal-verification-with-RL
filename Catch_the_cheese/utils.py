import csv
import os
import subprocess
import parameters_run



def validActions(user_po,PR):
    size = PR.get_size()
    valid = []
    pos = [0 for i in range(2)]
    if legalActions(0, user_po,PR):
        pos[0] = user_po - 1
        valid.append(0)
    if legalActions(1, user_po,PR):
        pos[1] = user_po + 1
        valid.append(1)

    return valid, pos


def writeStart(filename,PR):
    if os.path.exists(filename):
        os.remove(filename)  # create new file

    # write beginning of smv file
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	currentPosition : ")
        lw = '{'
        for i in range(PR.get_size()):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	score : ")
        lw = '{'
        for i in range(PR.get_score() + 2):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("\n\nASSIGN")

        fw.write(
            "			\n\n	init(currentPosition) := " + str(PR.get_start_point_model_checker()) + ";")

        # this is the counter
        fw.write("			\n\n	init(score) := 0;\n\n")

        fw.write("    next(currentPosition) := case\n")


def bestActions(q_line, user_po,PR):
    actionList = []
    bestactionlist = []

    if legalActions(0, user_po,PR):
        bestactionlist.append(user_po - 1)
    if legalActions(1, user_po,PR):
        bestactionlist.append(user_po + 1)

    return bestactionlist


def legalActions(index, user_po,PR):
    # the actions that are illegal:
    #   can't go up once you are at top of board
    #   can't go down once you are at bottom of board
    #   can't go left or right once you are at edge of board

    # left
    if index == 0 and user_po % PR.size != (0):
        return True
        # right
    if index == 1 and user_po % PR.size != (PR.size - 1):
        return True

    return False


def writePlayer(filename, listOfHoles, currentOptimal, Q,PR):
    if os.path.exists(filename):
        os.remove(filename)

    # write rest of smv file
    with open(filename, 'w') as fw:
        for i in range(len(listOfHoles)):
            fw.write(
                f"               currentPosition = " + str(listOfHoles[i]) + ": " + "{" + str(listOfHoles[i]) + "};\n")
        fw.write(
            f"               currentPosition = " + str(PR.size - 1) + f"&score<{PR.get_score()}" + ": " + "{" + str(PR.size - 2) + "};\n")
        fw.write(f"               currentPosition = " + str(PR.size - 1) + f"&score>={PR.get_score()}: " + "{" + str(PR.size - 1) + "};\n")
        for i in range(PR.size - 1):
            if i not in listOfHoles:
                bestMove = bestActions(Q[i], i,PR)
                fw.write(f"               currentPosition = " + str(i) + ": " + "{")
                lw = ""

                for i in range(len(bestMove)):
                    lw = lw + str(bestMove[i]) + ','

                # lw = lw + str(bestMove[0]) + ','
                lw = lw[:-1]
                lw = lw + "};\n"
                fw.write(lw)
        fw.write("               TRUE : currentPosition;\n")
        fw.write("    esac;\n\n")
        fw.write("    next(score) := case\n")
        fw.write(
            "               score = score&score<" + str(PR.get_score()) + "&currentPosition=" + str(PR.size - 1) + " : score+1;\n")
        fw.write("               TRUE : score;\n")
        fw.write("    esac;\n\n")

        # LTL line
        fw.write(f"LTLSPEC !F (score>={(PR.get_score())})\n")
        # fw.write("LTLSPEC F ((currentPosition ="+str(PR.size*PR.size-1)+")&(score<"+str(int(10*PR.size))+"))\n")


# main function of writing the smv file
def writeSmv(SIZE, currentOptimal, Q, listOfHoles, index,PR):
    filename_main = f"tests/test_t1_{index}.smv"
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{1}{SIZE}.txt'
        writeStart(filename_start,PR)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/{1}playersnextC{SIZE}.txt'
        writePlayer(filename_player, listOfHoles, currentOptimal, Q,PR)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)


# run smv file and check the result
def runSmv(index,PR):
    smv_file = f"test_t1_{index}.smv"
    os.chdir('tests')
    if os.name == 'nt':
        output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()  # on windows
    else:
        output = subprocess.check_output('nuXmv ' + smv_file, shell=True).splitlines()  # on linux
    os.chdir('../')
    ans = str(output[26][47:])[2:]
    ans = ans[0:len(ans) - 1]
    moveList = list()

    if 'false' in str(output):
        loop_vecs = str(b''.join(output))
        chunks = loop_vecs.split(' ')
        FLAG = False
        for i in range(len(chunks)):
            if chunks[i] == 'Counterexample':
                FLAG = True
            if chunks[i] == 'currentPosition' and FLAG:
                moveList.append((chunks[i + 2].strip("'")))

    return moveList, True, 0, 0


def writeStartPrism(filename, useNuxmv,PR):
    size = PR.get_size()
    if os.path.exists(filename):
        os.remove(filename)  # create new file

    # write beginning of prism file
    with open(filename, 'w') as fw:
        fw.write("dtmc\n\n")
        fw.write("module main\n\n")
        if useNuxmv == 1:
            fw.write("currentPosition : [0.." + str(size - 1) + "] init " + str(
                PR.get_start_point_model_checker()) + ";\n")
        else:
            fw.write("currentPosition : [0.." + str(size - 1) + "] init " + str(
                PR.get_start_point()) + " ;\n")
        fw.write("score : [0.." + str(PR.get_score() + 1) + "] init 0;\n\n")


def writePlayerPrism(filename, list_of_holes, q_table, probs,PR):
    size = PR.get_size()
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as fw:
        # next state value
        for i in range(len(list_of_holes)):  # if we're in a hole, we can't move
            fw.write("\t[] currentPosition=" + str(list_of_holes[i]) + " -> ")
            fw.write("(currentPosition'=" + str(list_of_holes[i]) + ");\n")
        # got to the end of the grid
        fw.write("\t[] currentPosition=" + str(size - 1) + f"&score<{PR.get_score()} -> ")
        fw.write("(currentPosition'=" + str(size - 2) + ");\n")
        fw.write("\t[] currentPosition=" + str(size - 1) + f"&score>={PR.get_score()} -> ")
        fw.write("(currentPosition'=" + str(size - 1) + ");\n")

        # rest of the states
        for i in range(size - 1):
            if i not in list_of_holes:  # not a hole
                bestMove = bestActions(q_table[i], i,PR)
                valid, pos = validActions(i,PR)  # get the valid actions and the next positions
                # create the string to write to the file
                str_to_write = "\t[] currentPosition=" + str(i) + " -> "
                if sum([probs[i][action] for action in valid]) == 0:  # all is zero - we didn't visit this state
                    for action in valid:
                        str_to_write += (
                                str(float(1) / len(valid)) + " : (currentPosition'=" + str(pos[action]) + ") + ")
                else:
                    for action in valid:
                        str_to_write += (str(probs[i][action]) + " : (currentPosition'=" + str(pos[action]) + ") + ")
                str_to_write = str_to_write[:-3] + ";\n"
                fw.write(str_to_write)

        # next score value
        # we didn't reach the end of the grid, and we have steps left
        str_to_write = "\n\t[] (score<" + str(PR.get_score()) + ")&(currentPosition=" + str(PR.size - 1) + ") -> (score'=(score + 1));\n"
        print(PR.get_score())
        # else - we reached the end of the grid, or we don't have steps left
        str_to_write += ("\t[] (score>=" + str(PR.get_score()) + ")|(currentPosition!=" + str(size - 1)
                         + ") -> (score'=score);\n\n")
        fw.write(str_to_write)

        fw.write("endmodule\n\n")


def writePrism(size, currentOptimal, q_table, listOfHoles, index, p, probs, useNuxmv,PR):
    size = PR.get_size()
    filename_main = f'tests/test_t1_{index}.prism'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/prism_add_start_{1}{size}{index}{p}.txt'
        writeStartPrism(filename_start, useNuxmv,PR)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/prism_{1}playersnextC{size}{index}{p}.txt'
        writePlayerPrism(filename_player, listOfHoles, q_table, probs,PR)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)

    props_file = f'tests/test_t1_{index}.props'
    with open(props_file, 'w') as fw:
        fw.write(f"P=? [(F (score>={PR.get_score()}))]\n")


def runPrism(index, results_file, PR):
    size = PR.get_size()
    filename = f'tests/test_t1_{index}.prism'
    props_file = f'tests/test_t1_{index}.props'
    result_file = f'tests/test_t1_{index}.res'
    # if os.path.exists(result_file):
    #     os.remove(result_file
    os.system(f'prism {filename} {props_file} -exportresults {result_file}')

    # save results to csv file
    csv_file = open(results_file, 'a', newline='')
    writer = csv.writer(csv_file)
    writer.writerow([open(result_file, 'r').readlines()[1].strip('\n')])
    csv_file.close()
