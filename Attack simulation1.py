import random
import numpy as np
import pandas as pd

#Attack simulation 1 
def generate_query_log():

    query_log = []
    time = 0

    num_users = 600
    adv_ratio = 0.2
    num_adv = int(num_users * adv_ratio)

    benign_users = [f"B{i}" for i in range(num_users - num_adv)]
    adv_users = [f"A{i}" for i in range(num_adv)]

    # ---------------- BENIGN ----------------
    for u in benign_users:
        seq = random.choices(nodes, k=40)

        for node in seq:
            time += np.random.exponential(scale=2.0)
            query_log.append([u, node, time, 0])

    # ---------------- ADVERSARY ----------------
    for u in adv_users:
        current = random.choice(nodes)

        for _ in range(40):

            r = random.random()

            if r < 0.3:
                node = random.choice(nodes)  # mimic benign
            elif r < 0.7:
                node = random.choice(list(G.neighbors(current))) if list(G.neighbors(current)) else random.choice(nodes)
            else:
                node = random.choice(nodes)

            current = node
            time += np.random.exponential(scale=1.5)

            query_log.append([u, node, time, 1])

    return pd.DataFrame(query_log, columns=["user", "node", "time", "label"])


df = generate_query_log()