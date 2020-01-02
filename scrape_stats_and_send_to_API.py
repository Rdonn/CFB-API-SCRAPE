from bs4 import BeautifulSoup
import requests
import mpu.io as mio
import configparser
import json
from re import sub
from time import time
class DataHolder: 
    def __init__(self):
        self.data = {}
        self.table_name = None
        self.url = None
    def add_to_data_json(self, hash_str, value): 
        hash_str = sub(r'[^a-zA-Z]', '', hash_str)
        if value == '-': 
            value = '0'
        self.data[hash_str] = value

    def set_table_name(self, name): 
        self.table_name = sub(r'[^a-zA-Z]', '', name)
        self.url = "http://" + api_host + "/statistics/" + self.table_name[0].lower() + self.table_name[1:]
    def print_data(self):
        print(json.dumps(self.data, indent=4))

configParser = configparser.ConfigParser()
configParser.read("current_config.ini")
api_host = configParser["host_information"]['host']
teams_id = mio.read('team_ids.json')
player_ids = mio.read('player_ids.json')

def gather_stats_for_player(source, player_id, year_played): 
    soup = BeautifulSoup(source)
    soup = BeautifulSoup(source, features='html.parser')
    captions = soup.find_all("caption")
    tables = soup.find_all("table", attrs={"class", "player-home"})
    
    #now we need to get the table headers inside of the tables
    table_headers = [[x.find_all("th"), x.find_all("td")] for x in tables] 

    for group in table_headers: 
        group[0] = [x.text for x in group[0]]
        group[1] = [x.text for x in group[1]]
    
    holder_to_iterate = {}
    for count ,group in enumerate(table_headers): 
        table_headers[count] = zip(*group)
        holder_to_iterate[captions[count].text] = list(table_headers[count])

    intermidiary_data_holder = []
    for x in holder_to_iterate: 
        data_holder = DataHolder()
        data_holder.set_table_name(x)
        data_holder.add_to_data_json("playerid",player_id)
        data_holder.add_to_data_json("yearplayed", year_played)
        data_holder.add_to_data_json("Split", str(time()))
        for header, value in holder_to_iterate[x]: 
            data_holder.add_to_data_json(header, value)
        intermidiary_data_holder.append(data_holder)
        
    return intermidiary_data_holder



    #weird formatting... so I will need to combine different parses
    

def get_player_home_index_page(team_year,team_id, player_id): 
    #example: http://www.cfbstats.com/2009/player/301/1024170/index.html
    return requests.get(url="http://www.cfbstats.com/{}/player/{}/{}/index.html".format(team_year,team_id, player_id)).text

def check_if_player_id_exists(team_name, team_year, id): 
    return str(id) in player_ids[team_year][team_name]

def get_players_by_team_name_and_year(name, year): 
    #example: http://localhost:3000/players/team?school=Clemson&year=2019
    return requests.get(url="http://localhost:3000/players/team", params={"school" : name, "year" : year})
    
def get_teams_by_conference(name, year): 
    #example: http://localhost:3000/teams/2019/Atlantic%20Coast%20Conference
    #returns back an array... so just pop the first entry. no way for this to fail as this script only uses API values that are guarenteed to have information
    return requests.get(url='http://localhost:3000/teams/{}/{}'.format(year, name)).json().pop(0)

def get_conferences(year): 
    #http://localhost:3000/conferences/2009
    return requests.get(url="http://localhost:3000/conferences/{}".format(year)).json()

def hackey_filer(url): 
    if "kickoffReturns" in url: 
        return str(url).replace('kickoffReturns', 'kickoffReturn')
    elif "puntReturns" in url: 
        return str(url).replace('puntReturns', 'puntReturn')
    else: 
        return url
if __name__ == '__main__':
    f = open('output.txt', 'w')
    for x in [y for y in range(2009, 2020)]:
        conferences = get_conferences(x)
        #now that we have the conferences, we need to get the teams
        for conf_data in conferences: 
            name = conf_data['name']
            year = conf_data['year']
            teams = get_teams_by_conference(name, year)
            for team_data in teams['teams']: 
                #now we need to get the team_id, which is stored locally in the script
                team_id = teams_id[team_data['name']]
                team_name = team_data['name']
                team_year = team_data['year']
                result = get_players_by_team_name_and_year(team_name, team_year).json()
                for player_data in result: 
                    if(check_if_player_id_exists(team_name, team_year, player_data['player_id'])): 
                        player_source = get_player_home_index_page(team_year,team_id, player_data['player_id'])
                        #this simple expects back a list of (json, url) to put the data in the DB through the API
                        results = gather_stats_for_player(player_source, player_data['player_id'], player_data['year_played'])

                        #now all we need to do is pass the resulting stuff through the requests library
                        for table_data in results: 
                            response = requests.put(url=hackey_filer(table_data.url), json=table_data.data)
                            if response.status_code >= 400: 
                                print('-' in table_data.data['G'], isinstance(table_data.data['G'], str))
                                print(table_data.data)
                                print(table_data.url)
                                print(response.status_code)
                                exit(1)
                print("Done with {} for year {}".format(team_name, team_year))
                        

            
    