'''
---------------------------------------------------------------------------------------------------------------------
Name:			RealtyModule.py

Version:		1.0-2

Author:			Seth Pruitt

Usage:			from RealtyModule import Get_Zillow_Data, Get_Homes

Description:	Provides library of functions for stream-lined use in other scripts relating to realty project.

Functions:		Get_Zillow_Data

					Description: Provides details on homes based on their address.

					Usage: Get_Zillow_Data(address, zipcode, Zkey)

					Params:	-address: Address as string.
							-zipcode: Zip code as string.
							-Zkey: Zillow API key as string.
					
					Returns: Dict object with the following parameters as strings:
								-Zillow ID
								-Zestimate
								-Lot Size
								-Square Feet
								-Bedrooms
								-Bathrooms
								-Year Built
								-Home Type
								-Listing Link
				
				Get_Homes

					Description: Provides a list of homes currently for sale on zillow within the provided area.

					Usage: Get_Homes(city-state)

					Params: city-state: The city-state abbreviation as stings. All lower case?

					Returns: List object containing a a dict object for home it finds. Dict contains the following:
								-Address
								-Zip Code
								-Asking Price

Comments:		10/09/2019 - Began writing module.

---------------------------------------------------------------------------------------------------------------------
'''

def Get_Zillow_Data(address, zipcode, Zkey):

	from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails

	zillow_data = ZillowWrapper(Zkey)
	deep_search_response = zillow_data.get_deep_search_results(address=address, zipcode=zipcode)
	result = GetDeepSearchResults(deep_search_response)
	#updated_property_details_response = zillow_data.get_updated_property_details(result.zillow_id)
	#updatedresult = GetUpdatedPropertyDetails(updated_property_details_response)
	resultdict = {'Zillow ID':result.zillow_id,
				  'Zestimate':result.zestimate_amount,
				  'Lot Size':result.property_size,
				  'Square Feet':result.home_size,
				  'Bedrooms':result.bedrooms,
				  'Bathrooms':result.bathrooms,
				  'Year Built':result.year_built,
				  'Home Type':result.home_type,
				  'Listing Link':result.home_detail_link}#,
				  #'Floors':updatedresult.num_floors,
				  #'Parking':updatedresult.parking_type,
				  #'Home Info':updatedresult.home_info,
				  #'School Info':updatedresult.school_district,
				  #'Neighborhood Info':updatedresult.neighborhood}
	return resultdict

def Get_Homes(city_state):

	import requests
	from bs4 import BeautifulSoup

	homesdata = []

	baseURL = 'https://www.zillow.com/'
	URL = baseURL + city_state + '/'
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

	pagable = True

	while pagable == True:
		page = requests.get(URL, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		
		homes = soup.find_all('article', 'list-card list-card-short list-card_not-saved')
		for home in homes:
			fulladdress = home.find("h3", "list-card-addr").contents[0]
			ztype = ', '.join(fulladdress[-5:]).replace(', ', '')
			if ztype.isdigit():
				zipcode = fulladdress[-5:]
				address = fulladdress[:-6]
				AskingPrice = home.find('div', 'list-card-price').contents[0]
				homesdata.append({'Address':address, 'Zip Code':zipcode, 'Asking Price':AskingPrice})
		
		pagination = soup.find("div", "search-pagination")
		pages = pagination.find_all("a")
		if pages[-1]['aria-label'] == 'NEXT Page':
			pagable = True
			NextPage = pages[-1]['href']
			URL = baseURL + NextPage
		else:
			pagable = False

	return homesdata