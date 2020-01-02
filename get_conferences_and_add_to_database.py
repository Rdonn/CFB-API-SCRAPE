import requests
from bs4 import BeautifulSoup
import configparser
from mpu import io

#example URL: http://www.cfbstats.com/2019/conference/index.html
conferences = {}

#accepts a list of what we are attempting to hit... in order
def createURL(data): 
    return "/".join(data)



def get_Conferences(year):
    url = "http://www.cfbstats.com/{}/conference/index.html".format(year)
    source = requests.get(url).text
    #soup.find("meta", {"name":"City"})
    soup = BeautifulSoup(source, features="html.parser").find("div", attrs={"id": "conferences"})
    soup = BeautifulSoup(str(soup), features="html.parser").find_all("a")
    conferences[str(year)] = [x.text for x in soup]


[get_Conferences(x) for x in range(2009, 2020)]

configParser = configparser.ConfigParser()
configParser.read("current_config.ini")

host = configParser["host_information"]['host']

for year in conferences: 
    for conference in conferences[year]: 
        url_args = [host, "conferences", str(year)]
        url = "http://" + createURL(url_args)

        response = requests.put(url, json={"conference_name": conference}, headers={"Content-Type": "application/json"})

        print(response.status_code)

