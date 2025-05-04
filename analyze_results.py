import pandas as pd
import matplotlib.pyplot as plt

# Load the combined dataset
file_path = 'generation_demand_combined_analysis_with_battery.csv'
combined_data = pd.read_csv(file_path)

# Key columns for analysis
demand = combined_data['Demand_kWh']
pv_generation = combined_data['PV_Generation_kWh']
wind_generation = combined_data['Wind_Generation_kWh']
net_balance = combined_data['Net_Balance_kWh']

# Total demand and generation
total_demand = demand.sum()
total_pv_generation = pv_generation.sum()
total_wind_generation = wind_generation.sum()
total_generation = total_pv_generation + total_wind_generation

# Self-sufficiency ratio
self_sufficiency = (total_generation / total_demand) * 100

# Calculate unmet demand and unused generation
unmet_demand = net_balance[net_balance < 0].abs().sum()
unused_generation = net_balance[net_balance > 0].sum()

# Battery storage simulation
battery_capacity = 2500  # Battery capacity in kWh
battery_level = 0
battery_discharge = []
battery_charge = []
battery_levels = []

# Hydrogen storage simulation
hydrogen_capacity = 10000000  # Hydrogen storage capacity in kWh equivalent
hydrogen_level = 0
electrolyzer_efficiency = 0.7  # Electrolyzer efficiency (70%)
fuel_cell_efficiency = 0.6  # Fuel cell efficiency (60%)
hydrogen_production = []
hydrogen_consumption = []
hydrogen_levels = []

for balance in net_balance:
    if balance > 0:  # Surplus energy
        # Battery charging
        charge = min(battery_capacity - battery_level, balance)
        battery_level += charge
        balance -= charge
        battery_charge.append(charge)
        battery_discharge.append(0)
        
        # Hydrogen production with remaining surplus
        hydrogen_generated = balance * electrolyzer_efficiency
        hydrogen_stored = min(hydrogen_capacity - hydrogen_level, hydrogen_generated)
        hydrogen_level += hydrogen_stored
        hydrogen_production.append(hydrogen_stored)
        hydrogen_consumption.append(0)
    else:  # Energy deficit
        # Battery discharging
        discharge = min(battery_level, abs(balance))
        battery_level -= discharge
        balance += discharge
        battery_discharge.append(discharge)
        battery_charge.append(0)
        
        # Hydrogen usage for remaining deficit
        hydrogen_used = min(hydrogen_level, abs(balance) / fuel_cell_efficiency)
        hydrogen_level -= hydrogen_used
        electricity_generated = hydrogen_used * fuel_cell_efficiency
        balance += electricity_generated
        hydrogen_production.append(0)
        hydrogen_consumption.append(hydrogen_used)

    # Record battery and hydrogen levels
    battery_levels.append(battery_level)
    hydrogen_levels.append(hydrogen_level)

# Add battery and hydrogen data to DataFrame
combined_data['Battery_Charge_kWh'] = battery_charge
combined_data['Battery_Discharge_kWh'] = battery_discharge
combined_data['Battery_Level_kWh'] = battery_levels
combined_data['Hydrogen_Production_kWh'] = hydrogen_production
combined_data['Hydrogen_Consumption_kWh'] = hydrogen_consumption
combined_data['Hydrogen_Level_kWh'] = hydrogen_levels

# Summary Statistics
print(f"Total Demand: {total_demand:.2f} kWh")
print(f"Total PV Generation: {total_pv_generation:.2f} kWh")
print(f"Total Wind Generation: {total_wind_generation:.2f} kWh")
print(f"Self-Sufficiency Ratio: {self_sufficiency:.2f}%")
print(f"Unmet Demand: {net_balance[net_balance < 0].abs().sum():.2f} kWh")
print(f"Unused Generation: {net_balance[net_balance > 0].sum():.2f} kWh")
print(f"Final Battery Level: {battery_level:.2f} kWh")
print(f"Final Hydrogen Level: {hydrogen_level:.2f} kWh equivalent")

# Save results to a new CSV file
combined_data.to_csv("updated_generation_demand_with_hydrogen.csv", index=False)

# Plot generation vs demand
plt.figure(figsize=(12, 6))
plt.plot(demand, label="Demand (kWh)", color='red', alpha=0.7)
plt.plot(pv_generation, label="PV Generation (kWh)", color='orange', alpha=0.7)
plt.plot(wind_generation, label="Wind Generation (kWh)", color='blue', alpha=0.7)
plt.title("Electricity Demand and Generation")
plt.xlabel("Time")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.tight_layout()
plt.show()

# Plot battery and hydrogen levels over time
plt.figure(figsize=(12, 6))
plt.plot(combined_data['Battery_Level_kWh'], label="Battery Level (kWh)", color='green', alpha=0.7)
plt.plot(combined_data['Hydrogen_Level_kWh'], label="Hydrogen Level (kWh)", color='purple', alpha=0.7)
plt.title("Battery and Hydrogen Levels Over Time")
plt.xlabel("Time")
plt.ylabel("Energy Storage (kWh)")
plt.legend()
plt.tight_layout()
plt.show()
