import google_scraper_with_location as gs
import pandas as pd
import csv
from datetime import date
import os


if __name__ == "__main__":

#poi_locations file contain ths locations for scrapping and types.csv contain the type of offices
    location_df = pd.read_csv('./poi_locations.csv')

    types_df = pd.read_csv('./types.csv')

    today = date.today()

    for index1, l in location_df.iterrows():

        try:

            district = l['district']
            area = l['area']
           

            latitude = l['latitude']
            longitude = l['longitude']

            search_location = str(latitude)+', '+str(longitude)

            print(district,area)

            for index2, t in types_df.iterrows():

                try:
                
                    type = str(t['type']).lower()

                    results = gs.get_data_from_google(search_location,type)

                    data_list = []
                    for result in results:
                        if result['place_name'] != '' and result['latitude'] != '' and result['longitude'] != '' and result['address'] != '':
                            data_list.append({
                                'place_name': result['place_name'],
                                'latitude': result['latitude'],
                                'longitude': result['longitude'],
                                'address': result['address'],
                                'phone_number': result['phone_number'],
                                'review_count': result['review_count'],
                                'ratings' : result['ratings']

            
                            })
                    print("----------------------------------------------------")
                    results_df = pd.DataFrame(data_list)
                    print(results_df)
                    with open('./scrapping_output/' + str(district) + '_' + str(area) + '.csv', 'a', newline='') as output:
                        if os.path.getsize(output.name) == 0:
                            results_df.to_csv(output, index=False)  # Write header + data
                        else:
                            results_df.to_csv(output, index=False, header=None, mode='a')  # Append data only

                   
                except:
                    pass

        except:
            pass