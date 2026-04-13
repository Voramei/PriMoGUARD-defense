import numpy as np
import networkx as nx
import pandas as pd

# Vanta Graph construction
V = nx.MultiDiGraph()

user_edges = defaultdict(list)
user_times = defaultdict(list)
pair_volume = defaultdict(int)

for _, row in df.iterrows():

    u, v, t = row["user"], row["node"], row["time"]

    V.add_node(u, type="user")
    V.add_node(v, type="target")

    V.add_edge(u, v, edge_type="query", timestamp=t)

    user_edges[u].append(v)
    user_times[u].append(t)
    pair_volume[(u, v)] += 1

# sort times
for u in user_times:
    user_times[u].sort()


G_structure = nx.Graph()
for u, v in G.edges():
    G_structure.add_edge(u, v)

K = 2

k_hop_neighbors = {
    n: set(nx.single_source_shortest_path_length(G_structure, n, cutoff=K).keys())
    for n in G_structure.nodes()
}

#Features extraction

def omega(u, v):
    return pair_volume.get((u, v), 0)

def omega_hat(u, v):
    deg = len(user_edges[u])
    return omega(u, v) / (deg + 1e-6)

def kappa(u, v):
    return sum(1 for x in user_edges[u] if x in k_hop_neighbors.get(v, set()))

def kappa_hat(u, v):
    deg = len(user_edges[u])
    return kappa(u, v) / (deg + 1e-6)

def phi(u):
    times = user_times[u]
    if len(times) <= 1:
        return 0.0
    return len(times) / (times[-1] - times[0] + 1e-6)

def theta(u):
    times = user_times[u]
    return np.mean(np.diff(times)) if len(times) > 1 else 0.0

def mu(u):
    return np.mean(user_times[u]) if len(user_times[u]) > 0 else 0.0

def tau(u, delta=5.0):
    times = user_times[u]
    m = mu(u)
    return sum(1 for t in times if abs(t - m) > delta)


def extract_features(u):

    targets = set(user_edges[u])

    omega_vals = [omega(u, v) for v in targets]
    omega_n = [omega_hat(u, v) for v in targets]

    kappa_vals = [kappa(u, v) for v in targets]
    kappa_n = [kappa_hat(u, v) for v in targets]

    influencer_vals = [len(target_users.get(v, set())) for v in targets]
    avg_influencer_count = np.mean(influencer_vals) if influencer_vals else 0

    normalized_influencer_vals = [len(target_users.get(v, set())) / (total_users + 1e-6) for v in targets]
    avg_normalized_influencer_count = np.mean(normalized_influencer_vals) if normalized_influencer_vals else 0

    return [
        np.mean(omega_vals) if omega_vals else 0.0,
        np.mean(omega_n) if omega_n else 0.0,
        np.mean(kappa_vals) if kappa_vals else 0.0,
        np.mean(kappa_n) if kappa_n else 0.0,
        avg_influencer_count,          
        avg_normalized_influencer_count, 
        phi(u),
        phi(u) / (max(phi(v) for v in user_edges.keys()) + 1e-6),
        theta(u),
        mu(u),
        tau(u)
    ]


users = list(user_edges.keys())

X = np.array([extract_features(u) for u in users])
X = np.nan_to_num(X)

y = np.array([1 if u.startswith("A") else 0 for u in users])

df_features = pd.DataFrame(X, columns=[
    "omega",
    "omega_norm",
    "kappa",
    "kappa_norm",
    "phi",
    "phi_norm",
    "theta",
    "mu",
    "unusual_time_count"
])

df_features["user"] = users

print("\n===== PRI-MOGUARD FEATURE SAMPLE =====\n")
print(df_features.head())