import os

for size in [10,15,20]:
    for j in range(0, 9):
        p = 1 - j * 0.05
        os.system(f"docker create --name c{size}{p} --rm -it -v $HOME:$HOME -v /opt/gurobi:/opt/gurobi -w $HOME/softmax ubuntu_python3.8:1 python3 main.py {p} {size}")  # This is the command that opens the docker container
        os.system(f"docker start c{size}{p}")  # This is the command that starts the docker container