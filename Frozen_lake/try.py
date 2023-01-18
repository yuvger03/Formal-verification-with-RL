import os

for i in range(10):
    for j in range(3):
        os.system(f"docker start c{i}{j}")  # This is the command that starts the docker container