# -*- coding: utf-8 -*-
# Luis A. Flores
# astroMapper.py
# Application to map distribution of possible galactic sources in the zone of avoidance.
# May 15, 2020

# J2000
# 18 04 01 .. 17 11 32
# -42 32 41 .. -9 49 52

# J1950
# 18 00 25 .. 17 08 47
# -42 32 50 .. -9 46 16 

import pandas as pd
from astropy.coordinates import SkyCoord  # High-level coordinates
import astropy.units as u
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
# from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
# from astropy.coordinates import Angle, Latitude, Longitude  # Angles
# from astropy.wcs import WCS
# import numpy as np

#Creating string list with file names in directory
filenames = ["Tables/SourcesTable_AllCoordinates.xlsx", "Tables/Durret.xlsx", "Tables/Hasegawa(2000).xlsx", 
             "Tables/Schroder(2019).xlsx", "Tables/Terzan(1988).xlsx", "Tables/Clusters.xlsx", "Tables/Nakanishi(1997).xlsx",
             "Tables/Meyer(2004).xlsx"]

#Creating empty lists to store values
dataframes = []; srcEqCoord=[]; srcGalCoord = []
#Iterable list of colors for scatter plot
colors = itertools.cycle(["#3a0be5", "green", "black", "#fd9a3c", "#e7c062", "yellow", "violet", "maroon"])

#Reading files and storing in dataframe array
for x in range(0, len(filenames), 1):
    dataframes.append(pd.read_excel(filenames[x]))
        
#Opening background .fits image
hdulist = fits.open('Images/SFL_-495_495.fits')
#Printing image information
header = hdulist[0].header
#Displaying image information
#print(hdulist.info()); print("\n"); print(header); print("\n")
#Extracting image data
img = hdulist[0].data
bg = img[:, :]
    
# Plot image
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.imshow(bg ** 0.3, extent=[-180., 180., -90., 90.], cmap='cool', origin='lower')

# Scatter plot loop
for x in range(0, len(dataframes), 1):
    if filenames[x] == "Tables/Hasegawa(2000).xlsx":
        #Reading and storing coordinate data from file and converting data to equatorial coordinates in degrees
        srcEqCoord.append(SkyCoord(ra=dataframes[x].Hms.to_list(), dec=dataframes[x].Dms.to_list(), unit=(u.hourangle, u.deg)))
        #Converting equatorial coordinates to galactic coordinates
        srcGalCoord.append(srcEqCoord[x].galactic)
    else:
        #Reading and storing coordinate data from file and converting data to equatorial coordinates in degrees
        srcEqCoord.append(SkyCoord(ra=dataframes[x].RA.to_list(), dec=dataframes[x].DEC.to_list(), unit=(u.deg, u.deg)))
        #Converting equatorial coordinates to galactic coordinates
        srcGalCoord.append(srcEqCoord[x].galactic)
    
    # print(len(srcGalCoord)) #list size
    # print(len(srcGalCoord[x])) #Size of list within the list (file rows)
    
    #Iterating to the next color in the colors list
    colorIter = next(colors)
    #Plotting the galactic coordinates
    ax.scatter(srcGalCoord[x].l.wrap_at(180*u.deg), srcGalCoord[x].b, s=9, edgecolor='none', facecolor=colorIter)
 
#Marking the cD Galaxy
ax.scatter(0.56370321, 9.27138298, marker='X', s=10, color='none', edgecolor='red', linewidths=0.5)
#Marking ro-Oph dark clouds
ax.scatter(-7, 16, marker='X', s=10, color='none', edgecolor='red', linewidths=0.5)
ax.annotate("Oph Cloud", (-7, 17), ha='center', textcoords="offset points", color='white', size=5, xytext=(0,-15))
#Creating Legend 
Flores = mpatches.Patch(facecolor='#3a0be5', label='Flores(2020)')    
Hasegawa = mpatches.Patch(facecolor='black', label='Hasegawa(2000)') 
Durret = mpatches.Patch(facecolor='green', label='Durret(2015-18)') 
Schroder = mpatches.Patch(facecolor='#fd9a3c', label='Schroder(2019)') 
Terzan = mpatches.Patch(facecolor='#e7c062', label='Terzan(1988)')   
Clusters = mpatches.Patch(facecolor='yellow', label='Star Clusters')
Nakanishi = mpatches.Patch(facecolor='violet', label='Nakanishi(1997)') #IRAS
Meyer = mpatches.Patch(facecolor='maroon', label='Meyer(2004)') #H1PASS
ax.legend(fontsize=5, handles=[Flores, Hasegawa, Durret, Schroder, Terzan, Clusters, Nakanishi, Meyer], 
            bbox_to_anchor=(1, 1), loc='upper left')

#Reading region coordinates from file
regionNames = ["cD", "II", "III", "IV", "V", "VI", "VII", "VIII", "Sag."]
regCoord=[]; galCoord=[]
regionFile = pd.read_excel("Tables/TableRegions.xlsx")
regCoord.append(SkyCoord(ra=regionFile.RA.to_list(), dec=regionFile.DEC.to_list(), unit=(u.hourangle, u.deg))) 

#Plotting circles and writing annotations
for x in range(0, 9, 1):
    galCoord.append(regCoord[0][x].galactic)    
    ax.scatter(galCoord[x].l.wrap_at(180*u.deg), galCoord[x].b, s=250, edgecolor='red', color='none', linewidths=0.5, alpha=0.5)
    ax.annotate(regionNames[x], (galCoord[x].l.wrap_at(180*u.deg).to_value(equivalencies=u.dimensionless_angles()),
                                 galCoord[x].b.to_value(equivalencies=u.dimensionless_angles())), ha='center', 
                 textcoords="offset points", color='white', size=5, xytext=(0,10))
    

#Plot configuration
ax.set_title("The Zone of Avoidance and the Ophiuchus Supercluster\nMilky Way HI Emission")
ax.grid(True)
ax.set_xlim(10., -10.)
ax.set_ylim(-5., 17.)
ax.set_xlabel('Galactic Longitude')
ax.set_ylabel('Galactic Latitude')
fig.savefig('Project_Sources_H1.png',bbox_inches='tight', dpi=1200)
