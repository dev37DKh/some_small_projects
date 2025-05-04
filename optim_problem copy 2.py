from pyomo.environ import *
import pandas as pd
# Create a Pyomo model
model = ConcreteModel()


file_path = 'generation_demand_combined_analysis_with_battery.csv'
combined_data = pd.read_csv(file_path)

demand = combined_data['Demand_kWh']
pv_profile = combined_data['PV_Generation_kWh']
wind_profile = combined_data['Wind_Generation_kWh']


combined_data.fillna(0, inplace=True)

# Sets
T = len(demand)  # Time periods
model.T = RangeSet(0, T-1)

# Decision Variables
model.C_PV = Var(domain=NonNegativeReals)  # PV capacity (kWp)
model.C_Wind = Var(domain=NonNegativeReals)  # Wind capacity (kWp)
model.C_Battery = Var(domain=NonNegativeReals)  # Battery capacity (kWh)
model.C_Hydrogen = Var(domain=NonNegativeReals)  # Hydrogen storage capacity (kWh equivalent)

model.Battery_Level = Var(model.T, domain=NonNegativeReals)  # Battery state of charge
model.Hydrogen_Level = Var(model.T, domain=NonNegativeReals)  # Hydrogen storage level

model.Battery_Charge = Var(model.T, domain=NonNegativeReals)
model.Battery_Discharge = Var(model.T, domain=NonNegativeReals)

model.Hydrogen_Production = Var(model.T, domain=NonNegativeReals)
model.Hydrogen_Consumption = Var(model.T, domain=NonNegativeReals)


model.Grid_Import = Var(model.T, domain=NonNegativeReals)  # Grid energy imported
model.Grid_Export = Var(model.T, domain=NonNegativeReals)  # Grid energy exported



# Objective Function: Minimize costs
cost_PV = 800  # Cost per kWp
cost_Wind = 1200  # Cost per kWp
cost_Battery = 300  # Cost per kWh
cost_Hydrogen = 150  # Cost per kWh equivalent

grid_cost_per_kWh = 10 # Example grid electricity price
model.Cost = Objective(
    expr=(model.C_PV * cost_PV +
         model.C_Wind * cost_Wind +
         model.C_Battery * cost_Battery +
         model.C_Hydrogen * cost_Hydrogen +
         sum(grid_cost_per_kWh * model.Grid_Import[t] for t in model.T))/1000,
    sense=minimize
)



# Constraints


def energy_balance_rule(model, t):
    pv_gen = pv_profile[t] * model.C_PV
    wind_gen = wind_profile[t] * model.C_Wind
    return (
        demand[t] + model.Grid_Export[t] ==
        pv_gen + wind_gen + model.Battery_Discharge[t] + model.Hydrogen_Consumption[t] + model.Grid_Import[t]
    )
model.EnergyBalance = Constraint(model.T, rule=energy_balance_rule)



battery_charge_efficiency = 0.95
battery_discharge_efficiency = 0.95

def battery_dynamics_rule(model, t):
    if t == 0:
        return model.Battery_Level[t] == (
            battery_charge_efficiency * model.Battery_Charge[t] -
            (1 / battery_discharge_efficiency) * model.Battery_Discharge[t]
        )
    else:
        return (
            model.Battery_Level[t] ==
            model.Battery_Level[t-1] +
            battery_charge_efficiency * model.Battery_Charge[t] -
            (1 / battery_discharge_efficiency) * model.Battery_Discharge[t]
        )
model.BatteryDynamics = Constraint(model.T, rule=battery_dynamics_rule)


electrolyzer_efficiency = 0.70
fuel_cell_efficiency = 0.60

def hydrogen_dynamics_rule(model, t):
    if t == 0:
        return model.Hydrogen_Level[t] == (
            electrolyzer_efficiency * model.Hydrogen_Production[t] -
            (1 / fuel_cell_efficiency) * model.Hydrogen_Consumption[t]
        )
    else:
        return (
            model.Hydrogen_Level[t] ==
            model.Hydrogen_Level[t-1] +
            electrolyzer_efficiency * model.Hydrogen_Production[t] -
            (1 / fuel_cell_efficiency) * model.Hydrogen_Consumption[t]
        )
model.HydrogenDynamics = Constraint(model.T, rule=hydrogen_dynamics_rule)


model.PV_Surplus = Var(model.T, domain=NonNegativeReals)

def pv_generation_rule(model, t):
    return pv_profile[t] * model.C_PV == (
        model.Battery_Charge[t] +
        model.Hydrogen_Production[t] +
        model.PV_Surplus[t]
    )
model.PVGeneration = Constraint(model.T, rule=pv_generation_rule)


# Solve the model
from pyomo.opt import SolverFactory
opt = SolverFactory('ipopt')  # Use any LP solver like GLPK or CBC
results = opt.solve(model, tee=True)

# Print Results
print("Optimal PV Capacity (kWp):", model.C_PV())
print("Optimal Wind Capacity (kWp):", model.C_Wind())
print("Optimal Battery Capacity (kWh):", model.C_Battery())
print("Optimal Hydrogen Capacity (kWh):", model.C_Hydrogen())
