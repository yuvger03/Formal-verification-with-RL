import os

for i in range(10):
    for j in range(3):
        os.system(f"docker create --name c{i*10+j*3} --rm -v $HOME:$HOME -w $HOME/project/Frozen_lake rl_image:latest python3 main.py {0.99 - 0.01*j} {1-i*0.01} {i*10+j*3}")  # This is the command that opens the docker container
        # os.system("python3 main.py")  # This is the command that runs the main.py file
        # os.system("cd ..")  # This is the command that goes back to the parent directory
        os.system(f"docker start c{i*10+j*3}")  # This is the command that starts the docker container