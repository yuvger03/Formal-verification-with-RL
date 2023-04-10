import csv
import os
from pickle import FALSE
import subprocess
import numpy as np
from action import Action
import parameters_run
SIZE=parameters_run.get_size()
import environment
import math

def validActions(user_po):
    size = parameters_run.get_size()
    valid = []
    pos = [0 for i in range(2)]
    if legalActions(0, user_po):
        pos[0] = user_po - 1
        valid.append(0)
    if legalActions(1, user_po):
        pos[1] = user_po + 1
        valid.append(1)

    return valid, pos
def writeStart(filename):
    if os.path.exists(filename):
        os.remove(filename)  #create new file

    #write beginning of smv file
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	currentPosition : ")
        lw = '{'
        for i in range(SIZE):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	score : ")
        lw = '{'
        for i in range(12):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("\n\nASSIGN")

        fw.write("			\n\n	init(currentPosition) := "+str(parameters_run.get_start_point_model_checker())+ ";")

        #this is the counter 
        fw.write("			\n\n	init(score) := 0;\n\n")

        fw.write("    next(currentPosition) := case\n")

def bestActions(q_line,user_po):
    actionList=[]
    bestactionlist=[]
    
    if legalActions(0,user_po):
     bestactionlist.append(user_po-1)
    if legalActions(1,user_po):
     bestactionlist.append(user_po+1)
    
    return bestactionlist


def legalActions(index,user_po):
    #the actions that are illegal:
    #   can't go up once you are at top of board
    #   can't go down once you are at bottom of board
    #   can't go left or right once you are at edge of board
    
        #left
    if index==0 and user_po%SIZE!=(0):
        return True
        #right
    if index==1 and user_po%SIZE!=(SIZE-1):
        return True
      
    return False

def writePlayer(filename, listOfHoles, currentOptimal, Q):
    if os.path.exists(filename):
        os.remove(filename)
    
    #write rest of smv file
    with open(filename, 'w') as fw:
        for i in range(len(listOfHoles)):
            fw.write(f"               currentPosition = "+ str(listOfHoles[i])+ ": " + "{" + str(listOfHoles[i]) + "};\n")
        fw.write(f"               currentPosition = "+ str(SIZE-1)+"&score<9"+ ": " + "{" + str(SIZE-2) + "};\n")
        fw.write(f"               currentPosition = "+ str(SIZE-1)+ "&score>=10: " + "{" + str(SIZE-1) + "};\n")
        for i in range(SIZE-1):
            if i not in listOfHoles:
                bestMove=bestActions(Q[i],i)
                fw.write(f"               currentPosition = "+ str(i) + ": " + "{")
                lw = ""
                
                for i in range(len(bestMove)):
                    lw = lw + str(bestMove[i]) + ','
                
                #lw = lw + str(bestMove[0]) + ','
                lw = lw[:-1]
                lw = lw + "};\n"
                fw.write(lw)
        fw.write("               TRUE : currentPosition;\n")
        fw.write("    esac;\n\n")
        fw.write("    next(score) := case\n")
        fw.write("               score = score&score<" +str(10) +"&currentPosition="+str(SIZE-1)+" : score+1;\n")
        fw.write("               TRUE : score;\n")
        fw.write("    esac;\n\n")

        #LTL line
        fw.write("LTLSPEC !F (score>=10)\n")
        #fw.write("LTLSPEC F ((currentPosition ="+str(SIZE*SIZE-1)+")&(score<"+str(int(10*SIZE))+"))\n")


# main function of writing the smv file
def writeSmv(SIZE, currentOptimal, Q, listOfHoles,index):
    filename_main = f"tests/test_t1_{index}.smv"
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{1}{SIZE}.txt'
        writeStart(filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/{1}playersnextC{SIZE}.txt'
        writePlayer(filename_player, listOfHoles, currentOptimal, Q)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)


# run smv file and check the result
def runSmv():
    smv_file = f'test_t1.smv'
    os.chdir('tests')
    output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()
    os.chdir('../')
    ans = str(output[26][47:])[2:]
    ans = ans[0:len(ans) - 1]
    moveList=list()
   
    if 'false' in str(output):
        loop_vecs = str(b''.join(output))
        chunks = loop_vecs.split(' ')
        FLAG=False
        for i in range(len(chunks)) :
            if chunks[i] == 'Counterexample':
                FLAG=True
            if chunks[i]== 'currentPosition' and FLAG:
                moveList.append((chunks[i+2]))
        
    return moveList,True,0,0

def writeStartPrism(filename):
    size = parameters_run.get_size()
    if os.path.exists(filename):
        os.remove(filename)  # create new file

    # write beginning of prism file
    with open(filename, 'w') as fw:
        fw.write("dtmc\n\n")
        fw.write("module main\n\n")
        fw.write("currentPosition : [0.." + str(size - 1) + "] init "+str(parameters_run.get_start_point_model_checker())+" ;\n")
        fw.write("score : [0.." + str(size+1) + "] init 0;\n\n")


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
        fw.write("\t[] currentPosition=" + str(size - 1) + "&score<9 -> ")
        fw.write("(currentPosition'=" + str(size - 2) + ");\n")
        fw.write("\t[] currentPosition=" + str(size - 1) + "&score>=10 -> ")
        fw.write("(currentPosition'=" + str(size - 1) + ");\n")

        # rest of the states
        for i in range(size - 1):
            if i not in list_of_holes:  # not a hole
                bestMove = bestActions(q_table[i], i)
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

        # next score value
        # we didn't reach the end of the grid, and we have steps left
        str_to_write = "\n\t[] (score<" +str(10) +"&currentPosition="+str(SIZE-1)+ ") -> (score'=(score + 1));\n"
        # else - we reached the end of the grid, or we don't have steps left
        str_to_write += ("\t[] (score>=" + str(10) + ")|(currentPosition!=" + str(size - 1)
                         + ") -> (score'=score);\n\n")
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
        fw.write("P=? [!(F (score>=10))]\n")


def runPrism(index, results_file):
    size = parameters_run.get_size()
    filename = f'tests/test_t1_{index}.prism'
    props_file = f'tests/test_t1_{index}.props'
    result_file = f'tests/test_t1_{index}.res'
    if os.path.exists(result_file):
        os.remove(result_file)
    os.system(f'prism {filename} {props_file} -exportresults {result_file}')

    # save results to csv file
    csv_file = open(results_file, 'a', newline='')
    writer = csv.writer(csv_file)
    writer.writerow([open(result_file, 'r').readlines()[1].strip('\n')])
    csv_file.close()