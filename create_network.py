import numpy as np
import random
import pickle
# import matplotlib
# matplotlib.use('QtAgg')
# import matplotlib.pyplot as plt
# from matplotlib.patches import Arc

def decimal_degrees_to_dms(decimal_degrees):
    if decimal_degrees < 0:
        decimal_degrees+=360
    degrees = int(decimal_degrees)
    minutes_float = abs(decimal_degrees - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    return degrees, minutes, seconds

def generate_connected_particles(n, xmin, xmax, ymin, ymax, seed=157):
    random.seed(seed)
    assert n >= 3, "Potrzeba co najmniej 3 punktów dla więzów kątowych."

    # 1. Losuj pozycje
    particles = [np.array([random.uniform(xmin, xmax), random.uniform(ymin, ymax)], dtype=np.float32) for _ in range(n)]

    # 2. Połącz punkty liniami w postaci grafu z przynajmniej jedną spójną składową
    linear_springs = []
    connected = set()
    connected.add(0)

    while len(connected) < n:
        i = random.choice(list(connected))
        j = random.choice([idx for idx in range(n) if idx not in connected])
        length = np.linalg.norm(particles[i] - particles[j])+0.0
        linear_springs.append((i, j, length))
        connected.add(j)

    # Dodaj dodatkowe losowe połączenia dla większej wyznaczalności
    while len(linear_springs) < 3 * n:
        i, j = random.sample(range(n), 2)
        if i != j and all((a, b) != (i, j) and (a, b) != (j, i) for a, b, _ in linear_springs):
            length = np.linalg.norm(particles[i] - particles[j])
            linear_springs.append((i, j, length))

    # 3. Kąty: wybierz losowe trójki sąsiadujących punktów (łączących się w środku)
    angular_springs = []
    used = set()
    for _ in range(2*n):
        center = random.randint(0, n - 1)
        neighbors = [i for i, j, _ in linear_springs if j == center] + [j for i, j, _ in linear_springs if i == center]
        if len(neighbors) >= 2:
            p1, p3 = random.sample(neighbors, 2)
            if (p1, center, p3) not in used:
                v1 = particles[p1] - particles[center]
                v2 = particles[p3] - particles[center]
                angle = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))+np.random.random()*0.0055
                angular_springs.append((p1, center, p3, angle))
                used.add((p1, center, p3))

    return particles, linear_springs, angular_springs

def save_data_4_snap(particles, linear_springs, angular_springs):
    with open("coords.crd", 'w') as f:
        f.write("Verlet Snap reference\n")
        f.write("UTMXXX\n")
        f.write("options no_geoid\n\n")
        for i, p in enumerate(particles):
            f.write(f"P{i}\t{p[0]:.4f}\t{p[1]:.4f}\t0.0\n")
    with open("pygame/distances", 'w') as f:
        f.write("Distances\n")
        f.write("#data hd\n")
        f.write("#ds_error 5.0 mm 1.0 ppm\n\n")
        for i, j, d in linear_springs:            
            f.write(f"P{i}\t0.0\tP{j}\t0.0\t{d:.4f}\n")
        f.write("\n#data ha no_heights\n")
        f.write("#ha_error 5 sec\n\n")
        for i, c, j, a in angular_springs:
            f.write(f"P{c}\n")
            f.write(f"P{j}\t0 00 00.0\n")
            a=np.degrees(a)
            d, m, s = decimal_degrees_to_dms(a)
            f.write(f"P{i}\t{d:02d} {m:02d} {s:.3f}\n")
    
def vector_angle(v):    
    return np.degrees(np.arctan2(v[1], v[0]))
        

if __name__=="__main__":
    particles, lin_springs, ang_springs = generate_connected_particles(n=30, xmin=100, xmax=700, ymin=100, ymax=500)
    # fig, ax = plt.subplots(figsize=(10, 10))
    for i, p in enumerate(particles):
        print(f"Particle {i}: {p}")
        # plt.text(p[0]+5,p[1]+5,str(i),fontsize=14)
    # plt.scatter([p[0] for p in particles], [p[1] for p in particles], s=100)
    # plt.scatter([particles[0][0],particles[9][0]], [particles[0][1], particles[9][1]], s=200,color="green")    
    print("\nLinear springs:")
    for i, j, d in lin_springs:
        print(f"{i} <-> {j}, rest length = {d:.2f}")
        # plt.plot([particles[i][0], particles[j][0]], [particles[i][1], particles[j][1]], '--', linewidth=1, color="gray")

    print("\nAngular springs:")
    for i, c, j, a in ang_springs:    
        print(f"angle({i}-{c}-{j}) = {np.degrees(a):.6f}")
        v1=particles[i]-particles[c]
        v2=particles[j]-particles[c]
        theta1 = vector_angle(v1)
        theta2 = vector_angle(v2)
        # arc = Arc((particles[c][0], particles[c][1]), 20, 20, angle=0, theta1=theta2, theta2=theta1, lw=1, color='gray')
        # ax.add_patch(arc)
    # ax.set_aspect('equal')
    # plt.axis('off')
    # plt.tight_layout()
    save_data_4_snap(particles, lin_springs, ang_springs)
    # plt.show()
    with open("pygame/new_net.pickle","wb") as f:
        pickle.dump({"particles":particles, "linear":lin_springs, "angular":ang_springs}, f)
    
