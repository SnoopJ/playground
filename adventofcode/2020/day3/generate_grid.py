"""
An accessory script to generate a random grid for debugging purposes
"""
import random

N = random.randint(8, 15)
M = random.randint((0.5*N)//1, (1.5*N)//1)

for _ in range(M):
    print("".join("#" if random.random() < 0.25 else "." for _ in range(N)))
