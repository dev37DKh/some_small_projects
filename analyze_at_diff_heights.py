import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
load_data = pd.read_excel('Lastgang_DieProduktions_AG.xlsx', engine='openpyxl')

# Inspect the original column names
print("Original Columns:", load_data.columns)

load_data['Demand_kWh'] = load_data["[MW]"] * 1000  # Convert from MW to kWh

# Convert the time column to datetime format if necessary
if 'time' in load_data.columns:
    load_data['time'] = pd.to_datetime(load_data['time'])

# Resample load data to hourly averages
hourly_load = load_data.resample('H', on='time').mean()

# Load the merged generation dataset (already hourly)
generation_dataset = xr.open_dataset('merged_full_year_2023.nc')

# Extract solar radiation and wind speed from the dataset
solar_radiation = generation_dataset['ssrd'] / 3.6e6  # Convert from J/m² to kWh/m²
u10 = generation_dataset['u10']  # u-component of wind at 10m
v10 = generation_dataset['v10']  # v-component of wind at 10m

# Calculate wind speed at 10m
wind_speed_10m = np.sqrt(u10**2 + v10**2)

# Analyze wind speeds at different heights
h = 80  # Heights in meters
z0 = 0.03  # Roughness length for open terrain
alpha = 0.14  # Wind shear exponent

# Logarithmic wind profile
wind_speed_10m = wind_speed_10m * np.log(h / z0) / np.log(10 / z0)



# Assume solar panel area and efficiency for PV generation
solar_panel_area = 1  # 1 m²
panel_efficiency = 0.18  # 18% efficiency
pv_capacity_kWp = 1  # 1 MWp

# Calculate hourly PV generation (scaled by capacity)
hourly_pv_generation = solar_radiation.resample(valid_time='1H').mean() * solar_panel_area * panel_efficiency * pv_capacity_kWp

# Assume wind turbine specifications for wind generation
turbine_capacity_kW = 1  # 1 MW turbine
rotor_radius = 2  # Rotor radius in meters
swept_area = np.pi * rotor_radius**2  # Rotor swept area in m²
rho = 1.225  # Air density in kg/m³


capacity_factor = 0.25  # Assume 25% capacity factor for small turbines
# Calculate wind power generation
hourly_wind_generation = (
    0.5 * rho * swept_area * (wind_speed_10m**3).resample(valid_time='1H').mean()
)*capacity_factor / 1000  # Convert to kWh

# Combine load and generation data into a single DataFrame
hourly_pv_df = hourly_pv_generation.to_dataframe(name='PV_Generation_kWh').reset_index()
hourly_wind_df = hourly_wind_generation.to_dataframe(name='Wind_Generation_kWh').reset_index()

# Merge load, PV, and wind data
combined_data = hourly_load.merge(hourly_pv_df, left_on='time', right_on='valid_time', how='inner')
combined_data = combined_data.merge(hourly_wind_df, left_on='valid_time', right_on='valid_time', how='inner')

# Calculate net balance (generation - load)
combined_data['Net_Balance_kWh'] = combined_data['PV_Generation_kWh'] + combined_data['Wind_Generation_kWh'] - combined_data['Demand_kWh']


# Save updated data for further analysis
combined_data.to_csv("generation_demand_combined_analysis_with_battery.csv", index=False)

'''
# Define battery parameters
battery_capacity = 10000  # Battery capacity in kWh (10 MWh)
battery_level = 0  # Initial battery charge (kWh)
battery_charge_rate = 5000  # Maximum charge/discharge rate in kWh per hour
time_step = 1  # Time step in hours
unmet_demand = 0  # Track unmet demand (kWh)
unused_generation = 0  # Track unused generation (kWh)
battery_net_balance = []  # Track adjusted net balance

# Simulate battery operation
for index, row in combined_data.iterrows():
    net_balance = row['Net_Balance_kWh']
    
    if net_balance > 0:  # Surplus energy
        # Energy available for charging the battery
        potential_charge = min(net_balance, battery_capacity - battery_level, battery_charge_rate * time_step)
        battery_level += potential_charge  # Update battery level
        unused_generation += max(0, net_balance - potential_charge)  # Track unused generation
        battery_net_balance.append(net_balance - potential_charge)  # Adjust net balance after charging

    elif net_balance < 0:  # Deficit energy
        # Energy required to meet the deficit
        potential_discharge = min(abs(net_balance), battery_level, battery_charge_rate * time_step)
        battery_level -= potential_discharge  # Update battery level
        unmet_demand += max(0, abs(net_balance) - potential_discharge)  # Track unmet demand
        battery_net_balance.append(-potential_discharge)  # Adjust net balance after discharging

    else:
        # No surplus or deficit
        battery_net_balance.append(0)

# Add battery-adjusted net balance to the DataFrame
combined_data['Battery_Adjusted_Net_Balance_kWh'] = battery_net_balance


# Print summary metrics
print(f"Total Unmet Demand (kWh): {unmet_demand}")
print(f"Total Unused Generation (kWh): {unused_generation}")
print(f"Final Battery Level (kWh): {battery_level}")

# Visualize the net balance before and after battery adjustment
plt.figure(figsize=(12, 6))
plt.plot(combined_data['Net_Balance_kWh'], label='Original Net Balance', color='blue', alpha=0.7)
plt.plot(combined_data['Battery_Adjusted_Net_Balance_kWh'], label='Battery-Adjusted Net Balance', color='green', alpha=0.7)
plt.title("Net Balance Before and After Battery Adjustment")
plt.xlabel("Time")
plt.ylabel("Net Balance (kWh)")
plt.legend()
plt.tight_layout()
plt.show()


# Analyze wind speeds at different heights
heights = [50, 80, 100, 120]  # Heights in meters
z0 = 0.03  # Roughness length for open terrain
alpha = 0.14  # Wind shear exponent

# Logarithmic wind profile
def logarithmic_wind(v10, h, z0):
    return v10 * np.log(h / z0) / np.log(10 / z0)

# Power law wind profile
def power_law_wind(v10, h, alpha):
    return v10 * (h / 10) ** alpha

# Calculate wind speeds at different heights
log_wind_speeds = {h: logarithmic_wind(wind_speed_10m, h, z0) for h in heights}
power_wind_speeds = {h: power_law_wind(wind_speed_10m, h, alpha) for h in heights}

# Calculate wind power for each height
def calculate_wind_power(wind_speeds):
    return 0.5 * rho * swept_area * wind_speeds**3 / 1000  # Convert to kWh

log_wind_power = {h: calculate_wind_power(ws) for h, ws in log_wind_speeds.items()}
power_wind_power = {h: calculate_wind_power(ws) for h, ws in power_wind_speeds.items()}

# Summarize results
log_power_totals = {h: np.sum(ws) for h, ws in log_wind_power.items()}
power_power_totals = {h: np.sum(ws) for h, ws in power_wind_power.items()}

# Plot results
plt.figure(figsize=(12, 6))

# Plot wind power for logarithmic profile
for h, power in log_wind_power.items():
    power_1d = power.values.flatten()  # Ensure data is 1D
    plt.plot(power_1d, label=f'Logarithmic {h}m')

# Plot wind power for power law profile
for h, power in power_wind_power.items():
    power_1d = power.values.flatten()  # Ensure data is 1D
    plt.plot(power_1d, linestyle='--', label=f'Power Law {h}m')

plt.title("Wind Power Output at Different Heights")
plt.xlabel("Time")
plt.ylabel("Power Output (kWh)")
plt.legend()
plt.tight_layout()
plt.show()
# Print total energy production
print("Total Energy Production (Logarithmic Profile):", log_power_totals)
print("Total Energy Production (Power Law Profile):", power_power_totals)
'''