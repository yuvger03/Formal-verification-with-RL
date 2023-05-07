import os

for size in [10,15,20]:
    for j in range(0, 9):
        os.system(f"docker create --name c{size}{j} --rm -it -v $HOME:$HOME -v /opt/gurobi:/opt/gurobi -w $HOME/softmax ubuntu_python3.8:1 python3 main.py {j} {size}")  # This is the command that opens the docker container
        os.system(f"docker start c{size}{j}")  # This is the command that starts the docker container