import numpy as np 
import pandas as pd 


"""
..  module:: generate_predictable_city
    :synopsis: The file that creates the predictable_areas.csv file from the pollution_us_2000_2016.csv file, which assists
    in input validation for the state, county, and city parameters.
..  moduleauthor:: Haotian Wang <haotianwang@ufl.edu>
"""


# read the csv file into a dataframe
df = pd.read_csv('pollution_us_2000_2016.csv')

# summarising Groups in the DataFrame
diff_area = df.groupby(['State','County','City']).groups.keys()
diff_State = df.groupby(['State']).groups.keys()
diff_County = df.groupby(['County']).groups.keys()
diff_City = df.groupby(['City']).groups.keys()

print(f"This framework currently support prediction for {len(diff_area)} different cities/areas.")
print(f"Number of unique states: {len(diff_State)}")
print(f"Number of unique counties: {len(diff_County)}")
print(f"Number of unique cities: {len(diff_City)}")

# convert dict to dataframe
area_df = pd.DataFrame.from_dict(diff_area)

# write the dataframe to a csv file
area_df.to_csv('predictable_areas.csv', index = False, header=["State", "County", "City"])
