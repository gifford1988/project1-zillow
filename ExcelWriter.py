#import dependencies
from RealtyModule import Get_Zillow_Data, Get_Homes
import pandas as pd
import numpy as np
zkey = 'X1-ZWz1hey97qto23_4lr3d'

#get list of homes (be patient!)
homes = Get_Homes('atlanta-ga')
print("Get Homes Done!")

#Get zillow data for first 5 in list
addresses = []
zipcodes =[]
prices = []
estimates = []
sizes = []
footages = []
rooms = []
baths = []
yearbuilt = []
hometype = []

for home in homes:
    addresses.append(home['Address'])
    zipcodes.append(home['Zip Code'])
    prices.append(home['Asking Price'])
    ZillowData = Get_Zillow_Data(home['Address'], home['Zip Code'], zkey)
    estimates.append(ZillowData['Zestimate'])
    sizes.append(ZillowData['Lot Size'])
    footages.append(ZillowData['Square Feet'])
    rooms.append(ZillowData['Bedrooms'])
    baths.append(ZillowData['Bathrooms'])
    yearbuilt.append(ZillowData['Year Built'])
    hometype.append(ZillowData['Home Type'])
    
        
print('API calls complete!')

#Build dataframe
HouseHuntersDF = pd.DataFrame({'Address':addresses,
                               'Zip Code':zipcodes,
                               'Asking Price':prices,
                               'Zestimate':estimates,
                               'Lot Size (in acres)':sizes,
                               'Square Feet':footages,
                               'Bedrooms':rooms,
                               'Bathrooms':baths,
                               'Year Built': yearbuilt,
                               'Home Type': hometype})

#HouseHuntersDF["Lot Size (in acres)"] = HouseHuntersDF["Lot Size (in acres)"].map("{:.2f}".format)
HouseHuntersDF['Asking Price'] = HouseHuntersDF['Asking Price'].astype(str).str.replace(',','').str.extract('(\d+)')

print(HouseHuntersDF.head())

# write DataFrame to excel
HouseHuntersDF = HouseHuntersDF.set_index(['Address'])
HouseHuntersDF
writer = pd.ExcelWriter("HouseHuntersData.xlsx")
HouseHuntersDF.to_excel(writer)
writer.save()