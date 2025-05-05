import xarray as xr

# List of paths to the quarterly files
file_paths = [
    'lichtenau_full_year_2023_1.nc',
    'lichtenau_full_year_2023_2.nc',
    'lichtenau_full_year_2023_3.nc',
    'lichtenau_full_year_2023_4.nc'
]


# Merge files without Dask
merged_dataset = xr.open_mfdataset(file_paths, combine='by_coords', engine='netcdf4', chunks=None)

# Save the merged dataset into a new file
merged_dataset.to_netcdf('merged_full_year_2023.nc')

print("Merged dataset saved as 'merged_full_year_2023.nc'")

