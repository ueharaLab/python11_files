import json
import urllib.parse
import urllib.request
import pprint
import pandas as pd
import codecs

api_key={"X-API-KEY":"Bi0mpfnfqrVq6XttdXknIb8tTZTbxrLlebbRpBYg"}
url = 'https://opendata.resas-portal.go.jp/api/v1/prefectures'

req = urllib.request.Request(url, headers=api_key)

with urllib.request.urlopen(req) as response:
    pref_data = response.read()

pref_d = json.loads(pref_data.decode())

pref_code ={}
for p_data in pref_d["result"]:
    pref_code[p_data["prefName"]]= p_data["prefCode"]
print(pref_code)

p_name = input('都道府県名:')
url_base = 'https://opendata.resas-portal.go.jp/api/v1/tourism/foreigners/forFrom'
foreign_visitors=[]
years = [2012,2013,2014,2015,2016,2017,2018,2019]

p_code = pref_code[p_name]

for year in years:
    p = {'year':year,'prefCode':p_code, 'purpose': 1}
    url = url_base + '?' + urllib.parse.urlencode(p)
   
    req = urllib.request.Request(url, headers=api_key)

    with urllib.request.urlopen(req) as response:
        data = response.read()
    d = json.loads(data.decode())

    #pprint.pprint(d)

    #for foreigners in d['result']['changes']:
    #    print(foreigners)



    for foreigners in d['result']['changes']:
        #print(foreigners['countryName'], foreigners['data'])
        annual_value=0
        quarter_val = [0]*4
        for i,f in enumerate(foreigners['data']):
           annual_value += f['value']
           quarter_val[i]=f['value']
        #print(foreigners['countryName'], annual_value)
        foreign_visitors.append([p_name, year, foreigners['countryName'], annual_value]+quarter_val)


f_visitors_df = pd.DataFrame(foreign_visitors, columns=['都道府県名','年','国籍','年間訪問者数','第1四半期','第2四半期','第3四半期','第4四半期'])
with codecs.open("forign_visitors.csv", "w", "ms932", "ignore") as all_data:
    f_visitors_df.to_csv(all_data, index=False, encoding="ms932", mode='w', header=True)