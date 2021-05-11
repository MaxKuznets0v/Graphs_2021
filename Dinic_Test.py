from Dinic import read_capacity, Graph
import os
import time

dir = os.path.join(os.path.abspath(os.getcwd()), "Tests")

for filename in os.listdir(dir):
    cap = read_capacity(os.path.join(dir, filename))

    try:
        start = time.time()
        flow = Graph(cap, 0, len(cap) - 1).dinic(False)
        end = time.time()
        print(f"Test {filename}: {flow[0]}, time: {end - start}")
    except:
        print(f"Test {filename} failed")

