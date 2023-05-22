import os
i = 0
for size in [10,15,20,25,30,40]:
    for j in range(0, 21):
        p = 1 - j * 0.05
        i += 1
        os.system(f"docker create --name c{size}{p} --rm -it --cpu-period=100000 --cpu-quota=25000 -v $HOME:$HOME -w $HOME/Project/Catch_the_cheese rl_image:2 python3 main.py {p} {size} {i}")  # This is the command that opens the docker container
        os.system(f"docker start c{size}{p}")  # This is the command that starts the docker container
        # os.system(f"docker kill c{size}{p}")  # This is the command that starts the docker container
