import csv
import os
from pickle import FALSE
import subprocess
import numpy as np
from action import Action
import parameters_run

import environment
import math


# SMV
def writeStart(filename):
    SIZE = parameters_run.get_size()
    if os.path.exists(filename):
        os.remove(filename)  # create new file

    # write beginning of smv file
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	currentPosition : ")
        lw = '{'
        for i in range(SIZE * SIZE):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	countSteps : ")
        lw = '{'
        for i in range(SIZE * SIZE + 1):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("\n\nASSIGN")

        fw.write("			\n\n	init(currentPosition) := 0;")

        # this is the counter
        fw.write("			\n\n	init(countSteps) := 0;\n\n")

        fw.write("    next(currentPosition) := case\n")


def bestActions(q_line, user_po):
    SIZE = parameters_run.get_size()
    actionList = []
    bestactionlist = []
    """
    max=-math.inf
    for i in range(4):
        if q_line[i]>max and legalActions(i,user_po):
            actionList.clear()
            actionList.append(i)
            max=q_line[i]
        elif q_line[i]==max:
            actionList.append(i)
#0=left
#1=right
#2=up
#3=down
    for i in range(len(actionList)):
        #left
        if actionList[i]==0 and user_po%SIZE!=(0):
            bestactionlist.append(user_po-1)
        #right
        if actionList[i]==1 and user_po%SIZE!=(SIZE-1):
            bestactionlist.append(user_po+1)
        #up
        if actionList[i]==2 and user_po>(SIZE-1):
            bestactionlist.append(user_po-SIZE)
        #down
        if actionList[i]==3 and (SIZE*SIZE-SIZE)>user_po:
            bestactionlist.append(user_po+SIZE)
        
    if(len(bestactionlist)==0):
    """
    if legalActions(0, user_po):
        bestactionlist.append(user_po - 1)
    if legalActions(1, user_po):
        bestactionlist.append(user_po + 1)
    if legalActions(2, user_po):
        bestactionlist.append(user_po - SIZE)
    if legalActions(3, user_po):
        bestactionlist.append(user_po + SIZE)

    return bestactionlist


def validActions(user_po):
    size = parameters_run.get_size()
    valid = []
    pos = [0 for i in range(4)]
    if legalActions(0, user_po):
        pos[0] = user_po - 1
        valid.append(0)
    if legalActions(1, user_po):
        pos[1] = user_po + 1
        valid.append(1)
    if legalActions(2, user_po):
        pos[2] = user_po - size
        valid.append(2)
    if legalActions(3, user_po):
        pos[3] = user_po + size
        valid.append(3)

    return valid, pos


def legalActions(index, user_po):
    SIZE = parameters_run.get_size()
    # the actions that are illegal:
    #   can't go up once you are at top of board
    #   can't go down once you are at bottom of board
    #   can't go left or right once you are at edge of board

    # left
    if index == 0 and user_po % SIZE != (0):
        return True
        # right
    if index == 1 and user_po % SIZE != (SIZE - 1):
        return True
        # up
    if index == 2 and user_po > (SIZE - 1):
        return True
        # down
    if index == 3 and (SIZE * SIZE - SIZE) > user_po:
        return True
    return False


def writePlayer(filename, listOfHoles, currentOptimal, Q):
    SIZE = parameters_run.get_size()
    if os.path.exists(filename):
        os.remove(filename)

    # write rest of smv file
    with open(filename, 'w') as fw:
        for i in range(len(listOfHoles)):
            fw.write(
                f"               currentPosition = " + str(listOfHoles[i]) + ": " + "{" + str(listOfHoles[i]) + "};\n")
        fw.write(
            f"               currentPosition = " + str(SIZE * SIZE - 1) + ": " + "{" + str(SIZE * SIZE - 1) + "};\n")
        for i in range(SIZE * SIZE - 1):
            if i not in listOfHoles:
                bestMove = bestActions(Q[i], i)
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
        fw.write("    next(countSteps) := case\n")
        fw.write("               countSteps = countSteps&countSteps!=" + str(SIZE * SIZE) + "&currentPosition!=" + str(
            SIZE * SIZE - 1) + " : countSteps+1;\n")
        fw.write("               TRUE : countSteps;\n")
        fw.write("    esac;\n\n")

        # LTL line
        fw.write("LTLSPEC !F ((currentPosition =" + str(SIZE * SIZE - 1) + ")&(countSteps<" + str(
            currentOptimal - 1) + "))\n")
        # fw.write("LTLSPEC F ((currentPosition ="+str(SIZE*SIZE-1)+")&(countSteps<"+str(int(10*SIZE))+"))\n")


# main function of writing the smv file
def writeSmv(SIZE, currentOptimal, Q, listOfHoles, index):
    SIZE = parameters_run.get_size()
    filename_main = f'tests/test_t1_{index}.smv'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{1}{SIZE}{index}.txt'
        writeStart(filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/{1}playersnextC{SIZE}{index}.txt'
        writePlayer(filename_player, listOfHoles, currentOptimal, Q)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)


# run smv file and check the result
def runSmv(index):
    SIZE = parameters_run.get_size()
    smv_file = f'test_t1_{index}.smv'
    os.chdir('tests')
    output = subprocess.check_output([f'nuXmv', smv_file], shell=True).splitlines() #on windows
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
                moveList.append(chunks[i + 2])
        setOfMoves = set()
        TorF = True
        step = -1
        state = -1
        for i in range(len(moveList)):
            if moveList[i] in setOfMoves:
                state = i - 1
                if int(moveList[i - 1]) - int(moveList[i]) == 1:
                    TorF = False
                    step = 0
                    return moveList, TorF, int(moveList[i - 1]), step
                if int(moveList[i - 1]) - int(moveList[i]) == -1:
                    TorF = False
                    step = 1
                    return moveList, TorF, int(moveList[i - 1]), step
                if int(moveList[i - 1]) - int(moveList[i]) == SIZE:
                    TorF = False
                    step = 2
                    return moveList, TorF, int(moveList[i - 1]), step
                if int(moveList[i - 1]) - int(moveList[i]) == -SIZE:
                    TorF = False
                    step = 3
                    return moveList, TorF, int(moveList[i - 1]), step
            else:
                setOfMoves.add(moveList[i])
        if int(moveList[len(moveList) - 1]) == SIZE * SIZE - 1:
            return moveList, True, 0, 0
        else:
            if int(moveList[len(moveList) - 2]) - int(moveList[len(moveList) - 1]) == 1:
                return moveList, moveList, int(moveList[len(moveList) - 2]), 0
            if int(moveList[len(moveList) - 2]) - int(moveList[len(moveList) - 1]) == -1:
                return moveList, moveList, int(moveList[len(moveList) - 2]), 1
            if int(moveList[len(moveList) - 2]) - int(moveList[len(moveList) - 1]) == SIZE:
                return moveList, moveList, int(moveList[len(moveList) - 2]), 2
            if int(moveList[len(moveList) - 2]) - int(moveList[len(moveList) - 1]) == -SIZE:
                return moveList, moveList, int(moveList[len(moveList) - 2]), 3
    return moveList, False, 0, 0


# PRISM
def writeStartPrism(filename):
    size = parameters_run.get_size()
    if os.path.exists(filename):
        os.remove(filename)  # create new file

    # write beginning of prism file
    with open(filename, 'w') as fw:
        fw.write("dtmc\n\n")
        fw.write("module main\n\n")
        fw.write("currentPosition : [0.." + str(size * size - 1) + "] init 0;\n")
        fw.write("countSteps : [0.." + str(size * size) + "] init 0;\n\n")


def writePlayerPrism(filename, list_of_holes, q_table, probs):
    size = parameters_run.get_size()
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as fw:
        # next state value
        for i in range(len(list_of_holes)):  # if we're in a hole, we can't move
            fw.write("\t[] currentPosition=" + str(list_of_holes[i]) + " -> ")
            fw.write("(currentPosition'=" + str(list_of_holes[i]) + ");\n")
        # got to the end of the grid
        fw.write("\t[] currentPosition=" + str(size * size - 1) + " -> ")
        fw.write("(currentPosition'=" + str(list_of_holes[i]) + ");\n")

        # rest of the states
        for i in range(size * size - 1):
            if i not in list_of_holes:  # not a hole
                valid, pos = validActions(i)  # get the valid actions and the next positions
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

        # next countSteps value
        # we didn't reach the end of the grid, and we have steps left
        str_to_write = "\n\t[] (countSteps!=" + str(size * size) + ")&(currentPosition!=" + str(size * size - 1) \
                       + ") -> (countSteps'=(countSteps + 1));\n"
        # else - we reached the end of the grid, or we don't have steps left
        str_to_write += ("\t[] (countSteps=" + str(size * size) + ")|(currentPosition=" + str(size * size - 1)
                         + ") -> (countSteps'=countSteps);\n\n")
        fw.write(str_to_write)

        fw.write("endmodule\n\n")


def writePrism(size, currentOptimal, q_table, listOfHoles, index, probs):
    size = parameters_run.get_size()
    filename_main = f'tests/test_t1_{index}.prism'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/prism_add_start_{1}{size}{index}.txt'
        writeStartPrism(filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/prism_{1}playersnextC{size}{index}.txt'
        writePlayerPrism(filename_player, listOfHoles, q_table, probs)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)

    props_file = f'tests/test_t1_{index}.props'
    with open(props_file, 'w') as fw:
        fw.write("P=? [!(F ((currentPosition =" + str(size * size - 1) + ")&(countSteps<" + str(
            currentOptimal - 1) + ")))]\n")

def runPrism(index):
    size = parameters_run.get_size()
    filename = f'tests/test_t1_{index}.prism'
    props_file = f'tests/test_t1_{index}.props'
    result_file = f'tests/test_t1_{index}.res'
    if os.path.exists(result_file):
        os.remove(result_file)
    os.system(f'prism {filename} {props_file} -exportresults {result_file} -const SIZE={size}')
    csv_file = f'tests/test_t1_{index}.csv'
    csv_file = open(csv_file, 'a')

    writer = csv.writer(csv_file)
    writer.writerow([open(result_file, 'r').readlines()[1]])
    csv_file.close()



