import os

i = 0
for size in [10, 15, 20, 25, 30, 40]:
    for j in range(0, 21):
        p = 1 - j * 0.05
        p_name = "0." + ("0" + str(j * 5) if j < 2 else str(j * 5)) if j != 20 else "1.0"
        i += 1
        os.system(f"docker create --name c{size}{p_name} --rm -it --cpu-period=100000 --cpu-quota=25000 -v $HOME:$HOME -w $HOME/project/Catch_the_cheese rl_image:1 python3 main.py {p_name} {size} {i}")  # This is the command that opens the docker container
        os.system(f"docker start c{size}{p_name}")  # This is the command that starts the docker container
        # # os.system(f"docker kill c{size}{p}")  # This is the command that starts the docker container
