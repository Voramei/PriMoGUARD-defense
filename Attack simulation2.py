def generate_query_log_with_lira_patterns():
    """
    Generate query log where:
    - Adversary users = Those performing LiRA-style attacks (targeted, bursty, high influencer)
    - Benign users = Random walk behavior
    """
    query_log = []
    time = 0
    
    num_users = 300
    adv_ratio = 0.2
    num_adv = int(num_users * adv_ratio)
    num_benign = num_users - num_adv
    
    # Get high-degree nodes (potential influencers)
    degrees = dict(G.degree())
    high_degree_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:50]
    high_degree_nodes = [n for n, _ in high_degree_nodes]
    
    # BENIGN USERS: Random walk behavior
    print(f"Generating {num_benign} benign users...")
    for i in tqdm(range(num_benign), desc="Benign users"):
        user = f"B{i}"
        current = random.choice(nodes)
        
        for _ in range(30):  # 30 queries per user
            # Random walk with occasional jumps
            if random.random() < 0.7:
                neighbors = list(G.neighbors(current))
                if neighbors:
                    current = random.choice(neighbors)
            else:
                current = random.choice(nodes)
            
            time += np.random.exponential(scale=2.5)  # Slow, natural pace
            query_log.append({
                'user': user,
                'node': current,
                'time': time,
                'label': 0  # Benign
            })
    
    # ADVERSARY USERS: LiRA-style attacks (targeted, bursty, high influencer nodes)
    
    print(f"\nGenerating {num_adv} adversary users (LiRA attack patterns)...")
    for i in tqdm(range(num_adv), desc="Adversary users"):
        user = f"A{i}"
        
        for _ in range(30):  # 30 queries per user
            # LiRA attack pattern: Target high-influence nodes
            
            if random.random() < 0.7:  # 70% targeted attacks
                node = random.choice(high_degree_nodes)
            else:
                node = random.choice(nodes)
            
            # Bursty timing (faster, more frequent)
            time += np.random.exponential(scale=0.8)  # Fast, bursty
            query_log.append({
                'user': user,
                'node': node,
                'time': time,
                'label': 1  # Adversary (LiRA attacker)
            })
    
    df = pd.DataFrame(query_log)
    print(f"\nTotal queries generated: {len(df)}")
    print(f"Benign users: {df[df['label']==0]['user'].nunique()}")
    print(f"Adversary users: {df[df['label']==1]['user'].nunique()}")
    
    return df

df = generate_query_log_with_lira_patterns()

