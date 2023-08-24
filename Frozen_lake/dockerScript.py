import os

# for i in range(10):
for j in range(3):  # 0.99, 0.98, 0.97
    p_name = "0." + str(99 - j)
    os.system(f"docker create --name c{p_name} --rm -it --cpus='.25' -v $HOME:$HOME -w $HOME/project/Frozen_lake rl_image:1 python3 main.py {p_name} {j}")  # This is the command that opens the docker container
    # os.system("python3 main.py")  # This is the command that runs the main.py file
    # os.system("cd ..")  # This is the command that goes back to the parent directory
    os.system(f"docker start c{p_name}")  # This is the command that starts the docker container

for i in range(6):  # 0.95, 0.9, 0.85, 0.8, 0.75, 0.7
    p_name = "0." + str(95 - 5*i)
    os.system(f"docker create --name c{p_name} --rm -it --cpus='.25' -v $HOME:$HOME -w $HOME/project/Frozen_lake rl_image:1 python3 main.py {p_name} {i + 3}")  # This is the command that opens the docker container
    os.system(f"docker start c{p_name}")  # This is the command that starts the docker container