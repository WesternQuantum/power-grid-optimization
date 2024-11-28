from dimod import Binary, ConstrainedQuadraticModel, Integer
from config import edges, COST_PER_DISTANCE, nodes
from dwave.system import LeapHybridCQMSampler
import dwave.inspector

cqm = ConstrainedQuadraticModel()

# Store the binary variables for the flow and line activation
line_active_vars = {}
power_flow_vars = {}

# Define binary decision variables and power flow variables
for edge_name, edge_data in edges.items():
    # Binary variable for whether the line is active
    line_active = Binary(edge_name)  # 1 if active, 0 if not
    line_active_vars[edge_name] = line_active
    
    # Integer variable for power flow on the line, bounded by max power
    # Here we multiply by the binary variable line_active to set power flow when the line is active
    power_flow = Integer(f"flow_{edge_name}", lower_bound=0, upper_bound=edge_data["max_power"])
    power_flow_vars[edge_name] = power_flow
    
    # Add capacity constraint for each power line
    # cqm.add_constraint(line_active * power_flow <= edge_data["max_power"], label=f"capacity_{edge_name}")

    # Add cost to the objective
    cost = edge_data["distance"] * COST_PER_DISTANCE
    cqm.set_objective(line_active * cost)

# Power balance constraints for each node
for node_name, node_data in nodes.items():
    power_needed = node_data["power"]

    # Gather all incoming and outgoing flows for the node
    flow_in = []
    flow_out = []

    for edge_name, edge_data in edges.items():
        if edge_data["node1"] == node_name:  # Outgoing flow
            flow_out.append(power_flow_vars[edge_name])
        elif edge_data["node2"] == node_name:  # Incoming flow
            flow_in.append(power_flow_vars[edge_name])

    # Define the net power flow for the node
    # Sum of incoming flows minus the sum of outgoing flows should equal power_needed
    net_flow_expr = sum(flow_in) - sum(flow_out)

    # Add the power balance constraint to the CQM
    # cqm.add_constraint(net_flow_expr == power_needed, label=f"power_balance_{node_name}")

# Step 3: Solve the CQM
sampler = LeapHybridCQMSampler()
response = sampler.sample_cqm(cqm)

# Retrieve the best solution
best_solution = response.first.sample
print("Best Solution:", best_solution)

# Calculate total cost
total_cost = sum(edges[edge]["distance"] * COST_PER_DISTANCE for edge in edges if best_solution[edge] == 1)
print("Total Cost:", total_cost)