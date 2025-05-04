import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the merged dataset
file_path = 'merged_full_year_2023.nc'  # path to the file
dataset = xr.open_dataset(file_path)


# Extract solar radiation (ssrd) and wind components (u10, v10)
solar_radiation = dataset['ssrd'] / 3.6e6  # Convert from J/m² to kWh/m²
u10 = dataset['u10']  # u-component of wind at 10m
v10 = dataset['v10']  # v-component of wind at 10m

# Calculate 10m wind speed
wind_speed_10m = np.sqrt(u10**2 + v10**2)

# Update the time dimension name based on inspection
time_coord = 'Time'  

# Resample using the correct time coordinate
daily_solar_energy = solar_radiation.resample({time_coord: '1D'}).sum()
daily_wind_speed = wind_speed_10m.resample({time_coord: '1D'}).mean()

# Seasonal resampling
seasonal_solar_energy = solar_radiation.resample({time_coord: 'QS-DEC'}).sum()
seasonal_wind_speed = wind_speed_10m.resample({time_coord: 'QS-DEC'}).mean()



# Visualization for Solar Energy
daily_solar_energy.plot(label='Daily Solar Energy (kWh/m²)', color='orange')
plt.title("Daily Solar Energy Potential (kWh/m²)")
plt.xlabel("Date")
plt.ylabel("Energy (kWh/m²)")
plt.legend()
plt.show()

# Visualization for Wind Speed
daily_wind_speed.plot(label='Daily Wind Speed (m/s)', color='blue')
plt.title("Daily Wind Speed (10m height)")
plt.xlabel("Date")
plt.ylabel("Wind Speed (m/s)")
plt.legend()
plt.show()

# Combine seasonal solar and wind data
seasonal_solar_values = [float(value) for value in seasonal_solar_energy.values]
seasonal_wind_values = [float(value) for value in seasonal_wind_speed.values]
seasons = ["Winter", "Spring", "Summer", "Autumn", "Next Winter"]



print("Seasons:", seasons)
print("Seasonal Solar Values:", seasonal_solar_values)
print("Seasonal Wind Values:", seasonal_wind_values)
print("Length of seasons:", len(seasons))
print("Length of seasonal solar values:", len(seasonal_solar_values))
print("Length of seasonal wind values:", len(seasonal_wind_values))



# Bar chart for seasonal comparison
plt.bar(seasons, seasonal_solar_values, color='orange', alpha=0.7, label='Seasonal Solar Energy (kWh/m²)')
plt.bar(seasons, seasonal_wind_values, color='blue', alpha=0.7, label='Seasonal Wind Speed (m/s)', bottom=seasonal_solar_values)
plt.title("Seasonal Solar and Wind Energy Potential")
plt.xlabel("Season")
plt.ylabel("Energy (kWh/m²) / Wind Speed (m/s)")
plt.legend()
plt.show()

# Output key statistics
solar_stats = {
    "Daily Mean Solar Energy (kWh/m²)": daily_solar_energy.mean().item(),
    "Seasonal Mean Solar Energy (kWh/m²)": np.mean(seasonal_solar_values),
    "Total Annual Solar Energy (kWh/m²)": daily_solar_energy.sum().item()
}

wind_stats = {
    "Daily Mean Wind Speed (m/s)": daily_wind_speed.mean().item(),
    "Seasonal Mean Wind Speed (m/s)": np.mean(seasonal_wind_values),
    "Total Wind Data Points": len(daily_wind_speed)
}

# Display results as a DataFrame
results = pd.DataFrame({"Solar": solar_stats, "Wind": wind_stats})
print("Analysis Results:")
print(results)

# Save the results to a CSV file
results.to_csv("solar_wind_analysis_results.csv", index=False)
print("Results saved to 'solar_wind_analysis_results.csv'.")
