import os

for i in range(10):
    for j in range(3):
        os.system(f"docker create --name c{i},{j} --rm -v $HOME:$HOME -v /opt/gurobi:/opt/gurobi -w $HOME/softmax ubuntu_python3.8:1 python3 main.py {0.99 - 0.01*j} {0.05 +0.01*i} {i*10+j*3}")  # This is the command that opens the docker container
        # os.system("python3 main.py")  # This is the command that runs the main.py file
        # os.system("cd ..")  # This is the command that goes back to the parent directory
        os.system(f"docker start c{i}")  # This is the command that starts the docker container