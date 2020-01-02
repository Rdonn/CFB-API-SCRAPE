import requests
from bs4 import BeautifulSoup
import configparser
from mpu import io as mio

configParser = configparser.ConfigParser()
configParser.read("current_config.ini")
api_host = configParser["host_information"]['host']
teams_id = mio.read('team_ids.json')
player_ids = mio.read('player_ids.json')

fields_for_schema = {}

def parse_player_home_index_page(source):
    global fields_for_schema 
    soup = BeautifulSoup(source, features='html.parser')
    left_column = soup.find("div", attrs={"id":"leftColumn"}).find('div', attrs={'class':'section'})



    #weird formatting... so I will need to combine different parses
    header = left_column.find('li', attrs={'class':'header'})
    header_tops = left_column.find_all('li', attrs={'class':'header top'})
    to_search = [header]
    for x in header_tops: to_search.append(x)
    table_names = [x.text for x in to_search]
    
    results = left_column.find_all(lambda tag: tag.name == 'a' and tag.text.lower()=="split stats")
    
    for table_name, href in zip(table_names, results): 
        if table_name not in fields_for_schema: 
            fields_for_schema[table_name] = {}
            reference = href.attrs['href']
            url = "http://www.cfbstats.com" + reference
            #get the source for the link
            source = requests.get(url).text
            soup = BeautifulSoup(source) 
            result = soup.find('div', attrs={'class': 'split'}).find_all('th')
            columns = [x.text for x in result]
            for column_name in columns: 
                fields_for_schema[table_name][column_name] = None




    

def get_player_home_index_page(team_id, player_id): 
    #example: http://www.cfbstats.com/2009/player/301/1024170/index.html
    return requests.get(url="http://www.cfbstats.com/2009/player/{}/{}/index.html".format(team_id, player_id)).text

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



if __name__ == '__main__':
    #example for endpoint "http://localhost:3000/players/team?school=Clemson&year=2019"
    #i'm going to establish a pho list of statistics to see what is required by the database schema and what needs to be added
    
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
                        player_source = get_player_home_index_page(team_id, player_data['player_id'])
                        parse_player_home_index_page(player_source)
            break
        break
    
    mio.write('fields_for_schema.json', fields_for_schema)


    