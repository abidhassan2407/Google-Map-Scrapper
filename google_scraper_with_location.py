from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import extract_address as ea
import re
from datetime import datetime
from geopy.distance import geodesic
import traceback


current_time = datetime.now()

def get_data_from_google(search_location,poi_type):

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get("http://google.com/maps?hl=en")

    time.sleep(1)

    # chrome.maximize_window()

    time.sleep(3)

    search_box = chrome.find_element('xpath','//*[@id="searchboxinput"]')

    for i in search_location:
        search_box.send_keys(i)
        time.sleep(0.08)    
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)

    time.sleep(5)

    chrome.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/button').click()

    time.sleep(5)

    neareast_search_box = chrome.find_element('xpath','//*[@id="searchboxinput"]')

    # type = 'software company'

    for i in poi_type:
        neareast_search_box.send_keys(i)
        time.sleep(0.08)    
    time.sleep(2)
    neareast_search_box.send_keys(Keys.ENTER)

    time.sleep(5)


    end_text = 'None'

    new_elem = chrome.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')

    i=1
    while True:
        print(i,end_text)
        if end_text=="You've reached the end of the list." or i>=1700:
            chrome.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]').send_keys(Keys.ARROW_DOWN)
            chrome.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]').send_keys(Keys.ARROW_DOWN)
            time.sleep(2)
            break
        try:
            end_text = chrome.find_element('xpath','/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[243]/div/p').text
        except:
            pass
        chrome.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1)
        i+=1

    soup = BeautifulSoup(chrome.page_source, 'html.parser')

    time.sleep(2)

    chrome.quit()

    poi_list = []
    
    print(len(soup.find_all('a',href=True)))

    for link in soup.find_all('a',href=True):

        if str(link['href']).startswith('https://www.google.com/maps/place'):

            dict_obj = {
                "place_name_url":"",
                "place_name":"",
                "latitude":"",
                "longitude":"",
                "address":"",
                "url":"",
                "pType":""
             
            }
            
            place_url = link['href']

            # print (place_url)

            try:

                parsed_place_name = re.search('\/place\/(.+?)\/data', place_url)

                place_name_div = str(parsed_place_name.group(1)).replace('+',' ')

                parsed_location = re.search('[a-z]((2[0-6])\.\d+).+[a-z]((8[89]|9[0-3])\.\d+)',place_url)

                latitude = parsed_location.group(1)

                longitude = parsed_location.group(3)


                parsed_result = ea.get_results(place_name_div,latitude,longitude)
                
                for pr in parsed_result:
                    place_name = pr['name']
                    address = pr['address']
                    review_count = pr['review_count']
                    ratings = pr['ratings']
                    phone_number = pr["phone_number"]

                if geodesic((search_location),(pr['latitude'],pr['longitude'])).m<=3000:
                    dict_obj['place_name_url'] = place_name_div
                    dict_obj['latitude'] = latitude
                    dict_obj['longitude'] = longitude
                    dict_obj['address'] = address
                    dict_obj['place_name'] = place_name
                    dict_obj['url'] = place_url
                    dict_obj['pType'] = poi_type
                    dict_obj['review_count'] = review_count
                    dict_obj['ratings'] = ratings
                    dict_obj['phone_number'] = phone_number
              
                poi_list.append(dict_obj)
                # print(poi_list)

            except Exception:
                pass

    
    return poi_list