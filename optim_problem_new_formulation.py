from pyomo.environ import *
import pandas as pd
# Create a Pyomo model
model = ConcreteModel()


file_path = 'generation_demand_combined_analysis_with_battery.csv'
combined_data = pd.read_csv(file_path)

demand = combined_data['Demand_kWh']
pv_profile = combined_data['PV_Generation_kWh']
wind_profile = combined_data['Wind_Generation_kWh']




import casadi as ca
import numpy as np

# Parameters
T = len(demand)  # Time periods
cost_PV = 800
cost_Wind = 1200
cost_Battery = 300
cost_Hydrogen = 150

# Symbolic Variables
C_PV = ca.MX.sym('C_PV')
C_Wind = ca.MX.sym('C_Wind')
C_Battery = ca.MX.sym('C_Battery')
C_Hydrogen = ca.MX.sym('C_Hydrogen')

Battery_Level = ca.MX.sym('Battery_Level', T)
Hydrogen_Level = ca.MX.sym('Hydrogen_Level', T)
Battery_Charge = ca.MX.sym('Battery_Charge', T)
Battery_Discharge = ca.MX.sym('Battery_Discharge', T)
Hydrogen_Production = ca.MX.sym('Hydrogen_Production', T)
Hydrogen_Consumption = ca.MX.sym('Hydrogen_Consumption', T)

# Objective function
objective = (C_PV * cost_PV +
             C_Wind * cost_Wind +
             C_Battery * cost_Battery +
             C_Hydrogen * cost_Hydrogen)

# Constraints
constraints = []
for t in range(T):
    # Energy balance
    pv_gen = pv_profile[t] * C_PV
    wind_gen = wind_profile[t] * C_Wind
    constraints.append(
        pv_gen + wind_gen + Battery_Discharge[t] + Hydrogen_Consumption[t] >= demand[t]
    )

    # Battery dynamics
    if t == 0:
        constraints.append(
            Battery_Level[t] == Battery_Charge[t] - Battery_Discharge[t]
        )
    else:
        constraints.append(
            Battery_Level[t] ==
            Battery_Level[t-1] + Battery_Charge[t] - Battery_Discharge[t]
        )
    
    constraints.append(Battery_Level[t] <= C_Battery)

    # Hydrogen dynamics
    if t == 0:
        constraints.append(
            Hydrogen_Level[t] == Hydrogen_Production[t] - Hydrogen_Consumption[t]
        )
    else:
        constraints.append(
            Hydrogen_Level[t] ==
            Hydrogen_Level[t-1] + Hydrogen_Production[t] - Hydrogen_Consumption[t]
        )
    
    constraints.append(Hydrogen_Level[t] <= C_Hydrogen)

    # Renewable generation
    constraints.append(
        pv_profile[t] * C_PV >= Battery_Charge[t] + Hydrogen_Production[t]
    )

# Bounds
lbx = [0] * (4 + 6 * T)  # Lower bounds for variables
ubx = [ca.inf] * (4 + 6 * T)  # Upper bounds for variables

# Solve the problem
x = ca.vertcat(C_PV, C_Wind, C_Battery, C_Hydrogen,
               Battery_Level, Hydrogen_Level, Battery_Charge, Battery_Discharge,
               Hydrogen_Production, Hydrogen_Consumption)

nlp = {'x': x, 'f': objective, 'g': ca.vertcat(*constraints)}
solver = ca.nlpsol('solver', 'ipopt', nlp)

solution = solver(lbx=lbx, ubx=ubx)

# Extract the solution
optimal_C_PV = solution['x'][0]
optimal_C_Wind = solution['x'][1]
optimal_C_Battery = solution['x'][2]
optimal_C_Hydrogen = solution['x'][3]

print("Optimal PV Capacity (kWp):", optimal_C_PV)
print("Optimal Wind Capacity (kWp):", optimal_C_Wind)
print("Optimal Battery Capacity (kWh):", optimal_C_Battery)
print("Optimal Hydrogen Capacity (kWh):", optimal_C_Hydrogen)
