import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load combined data 
file_path = "generation_demand_combined_analysis.csv"
data = pd.read_csv(file_path)

# Extract relevant columns
demand = data['Demand_kWh']
net_balance = data['Net_Balance_kWh']  # Net balance = generation - demand

# Define battery parameters
battery_sizes = np.arange(0, 10001, 500)  # Battery capacities in kWh
results = []

for capacity in battery_sizes:
    battery_level = 0  # Initial battery charge
    unmet_demand = 0
    unused_generation = 0
    
    for balance in net_balance:
        if balance > 0:  # Surplus energy
            # Charge the battery with surplus
            charge = min(capacity - battery_level, balance)
            battery_level += charge
            unused_generation += balance - charge
        else:  # Deficit energy
            # Discharge the battery to meet demand
            discharge = min(battery_level, abs(balance))
            battery_level -= discharge
            unmet_demand += abs(balance) - discharge
    
    # Record results for this battery capacity
    results.append({
        "Battery_Capacity_kWh": capacity,
        "Unmet_Demand_kWh": unmet_demand,
        "Unused_Generation_kWh": unused_generation
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Replace or drop NaN values
results_df['Unmet_Demand_kWh'] = results_df['Unmet_Demand_kWh'].fillna(float('inf'))  # Replace NaN with a large number
# Alternatively: results_df.dropna(subset=['Unmet_Demand_kWh'], inplace=True)

# Find the optimal battery size (minimizing unmet demand)
optimal_size = results_df.loc[results_df['Unmet_Demand_kWh'].idxmin()]

# Save results to a CSV file
results_df.to_csv("battery_optimization_results.csv", index=False)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(results_df['Battery_Capacity_kWh'], results_df['Unmet_Demand_kWh'], label="Unmet Demand (kWh)", color='red')
plt.plot(results_df['Battery_Capacity_kWh'], results_df['Unused_Generation_kWh'], label="Unused Generation (kWh)", color='blue')
plt.axvline(optimal_size['Battery_Capacity_kWh'], color='green', linestyle='--', label=f"Optimal Size: {optimal_size['Battery_Capacity_kWh']} kWh")
plt.title("Battery Capacity Optimization")
plt.xlabel("Battery Capacity (kWh)")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.tight_layout()
plt.show()

# Print the optimal battery size and metrics
print("Optimal Battery Size (kWh):", optimal_size['Battery_Capacity_kWh'])
print("Unmet Demand (kWh):", optimal_size['Unmet_Demand_kWh'])
print("Unused Generation (kWh):", optimal_size['Unused_Generation_kWh'])
