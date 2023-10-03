from requests_html import HTMLSession
import re,json
from pyjsparser import parse
session = HTMLSession()
import time

# Return the list of address objects
def get_results(query_string,longitude,latitude):
    results=[]
    start=time.time()
    # url with query string
    r = session.get('https://www.google.com/maps/search/'+query_string.replace(' ','+')+'@'+str(latitude)+','+str(longitude)+',13z?hl=en')#@23.775069,90.3493016,13z')
    page_html=r.html
    #page=r.html.render() # you can use r.html.render(sleep=1) if you want
    # print(page_html)
    tag_with_text= page_html.find('script')
    # printing the element
    data=[]
    l=0
    for i in tag_with_text:
        #data.append(i.text)
        if len(i.text)>l: # get the max item considered as max exist
            data=[i.text]
            l=len(i.text)

    # with open("sample1.json", "w") as outfile:
    #     json.dump(parse(data[0]), outfile)
    sc=parse(data[0])['body'][0]['expression']['callee']['body']['body'][1]['expression']['right']['elements'][3]['elements'][2]['value']

    sc=json.loads(sc[5:])
    # with open("sample_data.json", "w") as outfile:
    #     json.dump(sc, outfile)
    sc_data={}
    for i in sc[0][1]:
        sc_data={}
        try:
            
            sc_data['name'] =i[14][11]
            sc_data['latitude'] =i[14][9][2]
            sc_data['longitude'] =i[14][9][3]
            sc_data['address'] =i[14][18]
            sc_data['review_count'] =i[14][4][-1]
            sc_data['reviews_URL'] =i[14][4][3][0]
            sc_data['ratings'] =i[14][4][-2]
            sc_data["phone_number"] = i[14][178][0][0]
            
        except Exception as e:
            print(e)
        if len(sc_data)>0:
            results.append(sc_data)
    end=time.time()
    # print(end-start)
    return results
if __name__ == "__main__":
    print(get_results('Brain Station 23','23.78154','90.40007'))