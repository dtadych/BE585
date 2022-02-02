# Packages to set up the enviornment
# Environment name: remsensdm

# %%
Packages = [pandas, 
            numpy, 
            time, 
            datetime, 
#            jupyterlab, 
            math, 
            matplotlib, 
            xlrd, 
            PIL,
            geopandas,
            xarray, 
            netCDF4, 
            rioxarray,
            rasterio
            cartopy]

for i in packages:
    conda install -c conda-forge  i
    print(i, "finished install")
