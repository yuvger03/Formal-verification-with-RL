import os

for i in range(10):
    for j in range(3):
<<<<<<< HEAD
        os.system(f"docker create --name c{i}{j} --rm -v $HOME:$HOME -w $HOME/project/Frozen_lake rl_image:latest python3 main.py {0.99 - 0.01*j} {0.05 +0.01*i} {i*10+j*3}")  # This is the command that opens the docker container
        # os.system("python3 main.py")  # This is the command that runs the main.py file
        # os.system("cd ..")  # This is the command that goes back to the parent directory
        os.system(f"docker start c{i}{j}")  # This is the command that starts the docker container
=======
        os.system(f"docker create --name c{i*10+j*3} --rm -v $HOME:$HOME -v /opt/gurobi:/opt/gurobi -w $HOME/softmax ubuntu_python3.8:1 python3 main.py {0.99 - 0.01*j} {0.14 +0.01*i} {i*10+j*3}")  # This is the command that opens the docker container
        # os.system("python3 main.py")  # This is the command that runs the main.py file
        # os.system("cd ..")  # This is the command that goes back to the parent directory
        os.system(f"docker start c{i*10+j*3}")  # This is the command that starts the docker container
>>>>>>> 7e7e02e32fe8c5e9131ad78ac7484ff7d99627b0
