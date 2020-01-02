from bs4 import BeautifulSoup
import requests
import mpu.io as mi
ids = {}

class Data_holder: 
    def __init__(self, year, conference_name, team_name):
        self.year = year
        self.conference_name = conference_name
        self.team_name = team_name
    def print_object(self): 
        print("year: {}, conference_name: {}, team_name: {}".format(self.year, self.conference_name, self.team_name))


relationships_to_add = []

def format_endpoint(year): 
    #sample endpoint: "http://localhost:3000/team/conferences/1234"
    return "http://localhost:3000/team/conferences/{}".format(year)

def handle_year(year): 
    #endpoint to scrape example: http://www.cfbstats.com/2019/team/index.html
    url = "http://www.cfbstats.com/{}/team/index.html".format(year)
    url_to_put_to = format_endpoint(year)

    soup = BeautifulSoup(requests.get(url).text, features="html.parser")

    #get all of the divisions we are interested in
    #the website uses identical ids for different things, so we will need to deal with that

    first_layer_divs = soup.find_all("div", attrs={"class":"conference"})
    for div in first_layer_divs: 
        #let us package this up in something nice... a small class would be usefull

        conference_name = div.find("h1").text
        for x in div.find_all("a"): 
            ids[x.text] = x['href'].split("/")[-2]
        teams = [team.text for team in div.find_all("a")]
        for x in teams: 
            #add them to the list of things to post later
            relationships_to_add.append(Data_holder(year, conference_name, x))


[handle_year(x) for x in range(2009, 2020)]
mi.write("team_ids.json",data=ids)
exit(1)
#go ahead and send them to the API
for x in relationships_to_add: 
    url = format_endpoint(x.year)
    requests.put(url, json={"conference_name":x.conference_name, "team_name":x.team_name})