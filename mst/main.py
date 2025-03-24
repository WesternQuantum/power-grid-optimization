import dimod

# from dwave.system import DWaveSampler, EmbeddingComposite

# USER INPUT: 2d matrix representing cost of each powerline, zero means no powerline
cost_matrix = [
    [0, 1, 2, 3],
    [1, 0, 4, 5],
    [2, 4, 0, 6],
    [3, 5, 6, 0],
]
n = len(cost_matrix)

# ensure that the cost matrix is symmetric
assert all(
    cost_matrix[i][j] == cost_matrix[j][i]
    for i in range(len(cost_matrix))
    for j in range(len(cost_matrix))
)

# create adjacency matrix from cost matrix
# matrix is assumed to be symmetric so only when i < j is the edge added
adjacency_matrix: list[list[str | int]] = []
for i in range(len(cost_matrix)):
    row = []
    for j in range(len(cost_matrix)):
        if cost_matrix[i][j] == 0:
            row.append(0)
        if i < j:
            row.append(f"A_{i}_{j}")
    adjacency_matrix.append(row)

# QUBO dictionary
Q = {}
offset = 0


# helper function to add to QUBO
def add_to_qubo(i, j, value):
    if (i, j) in Q:
        Q[(i, j)] += value
    else:
        Q[(i, j)] = value


# Config weights
lambda_1 = 49.9
lambda_2 = 100
lambda_c1 = 10000
lambda_c2 = 10000
lambda_aux = 10000


# helper function to create auxiliary variable
def create_aux_func(var1: str, var2: str) -> str:
    z12 = f"z_{var1}_{var2}"

    # z <=> var1 and var2
    # x1*x2 - 2(x1 + x2)*x + 3z
    add_to_qubo(var1, var2, lambda_aux)
    add_to_qubo(var1, z12, -2 * lambda_aux)
    add_to_qubo(var2, z12, -2 * lambda_aux)
    add_to_qubo(z12, z12, 3 * lambda_aux)

    return z12


# Cost penalty - uses lambda_1
for i in range(n):
    for j in range(n):
        if i < j and cost_matrix[i][j] != 0:
            add_to_qubo(f"A_{i}_{j}", f"A_{i}_{j}", lambda_1 * cost_matrix[i][j])


# Constraint 1: ensure A[i][j] == R[i][j]
for i in range(n):
    for j in range(n):
        if i < j:
            # lambda_2(A[i][j] - R[i][j])^2 == 0
            add_to_qubo(f"A_{i}_{j}", f"A_{i}_{j}", lambda_c1)
            add_to_qubo(f"R_{i}_{j}", f"R_{i}_{j}", lambda_c1)
            add_to_qubo(f"A_{i}_{j}", f"R_{i}_{j}", -2 * lambda_c1)

# Constraint 2: ensure R[i][j] <= R[i][k] * A[j][k] for all k
for i in range(n):
    for j in range(n):
        if i < j:
            for k in range(n):
                if j < k:
                    # lambda_2(Rij - Rik * Ajk)^2
                    aux_var = create_aux_func(f"R_{i}_{j}", f"R_{i}_{k}")

                    add_to_qubo(f"R_{i}_{j}", f"R_{i}_{j}", lambda_c2)
                    add_to_qubo(f"A_{j}_{k}", f"A_{j}_{k}", lambda_c2)
                    add_to_qubo(aux_var, f"A_{j}_{k}", -2 * lambda_c2)

# Reachability Penalty - uses lambda_2
for i in range(n):
    for j in range(n):
        if i < j:
            # lambda_2(1 - R[i][j])
            add_to_qubo(f"R_{i}_{j}", f"R_{i}_{j}", -lambda_2)
            offset += lambda_2

# Create BQM
bqm = dimod.BinaryQuadraticModel.from_qubo(Q, offset)

print("QUBO:")
print(bqm)

# solve bqm locally
sampler = dimod.ExactSolver()
response = sampler.sample(bqm)

lowest_energy_sample = response.first

print("Lowest energy sample:")

for key, value in lowest_energy_sample.sample.items():
    print(f"{key}: {value}")

print("Energy:", lowest_energy_sample.energy)
