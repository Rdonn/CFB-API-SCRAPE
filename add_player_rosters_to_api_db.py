from bs4 import BeautifulSoup
import requests
import json
import configparser
import mpu.io as mi

class DataHolder: 
    def __init__(self, team_name, year, conference, team_id): 
        self.team_name = team_name
        self.team_id = team_id
        self.year = year
        self.conference = conference

#hold all the data necessary to add to the DB through the API
class Player: 
    def __init__(self, p_id, number, name, pos, year, height, weight, hometown, last_school, school_name, school_year): 
        self.id = p_id
        self.number = number
        self.name = name
        self.pos = pos
        self.year = year
        self.height = height
        self.weight = weight
        self.hometown = hometown
        self.last_school = last_school
        self.school_name = school_name
        self.first_name = None
        self.last_name = None
        self.player_height_inches = None
        self.school_year = school_year
    def print_player(self): 
        print("|||".join([self.number, self.name, self.pos, self.year, self.height, self.weight, self.hometown, self.last_school]))


#get teams by conference year

#setup the host that we are hitting
parser = configparser.ConfigParser()
parser.read("current_config.ini")
method = "http:/"
host = parser['host_information']['host']

#get the reference ID's
ids = mi.read("team_ids.json")

#this object will be modified throughout the script
player_ids = {str(x):{} for x in range(2009, 2020)}
id_to_increment = 10006195

def format_player_for_api_and_send(player): 
    #we need the height in inches
    if not len(player.height) == 1: 
        height = player.height
        feet, inches = height.split("-")
        total_height = int(feet) * 12 + int(inches)
        player.player_height_inches = total_height
    else: 
        player.player_height_inches = "-"
    if not len(player.name) == 1: 
        name = player.name
        try:
            first_name = name.split(",")[-1].strip(" ")
            last_name = name.split(",")[0].strip(" ")
            player.last_name = last_name
            player.first_name = first_name
        except: 
            #weird name.. probably only 1 name
            player.first_name = player.name
            player.last_name = player.name
    """{
        "player_id": 0,
        "first_name": "string",
        "last_name": "string",
        "name": "string",
        "year": "string",
        "height": "string",
        "height_inches": 0,
        "weight": 0,
        "hometown": "string",
        "last_school": "string"
        }
    """
    #http://localhost:3000/players/1234/1234
    
    response = requests.post(create_url([method, host, "players", player.school_year, player.school_name]), 
                 json = {
                            "name": player.name,
                            "height": player.height,
                            "height_inches": player.player_height_inches,
                            "hometown": player.hometown,
                            "last_school": player.last_school, 
                            "pos": player.pos, 
                            "num": player.number
                            }, 
                headers={"Content-Type": "application/json", 
                         "accept": "application/json"})
    if response.status_code == 400: 
        player.print_player()
        temp = json.loads(response.request.body)
        print(json.dumps(temp, indent=4))
        exit("ERROR")

def parse_player(data, conference, team, year): 
    global id_to_increment
    to_check = data[1]
    id_to_add = None
    if to_check.find("a") is not None: 
        temp_id = to_check.find("a")['href'].split("/")[-2]
        if (player_ids[year].get(team) is None): 
            player_ids[year][team] = {}
        id_to_add = temp_id
        player_ids[year][team][temp_id] = None
    
    if id_to_add is None: 
        #we need to find a way to provide an ID to a player that does not have a link in website...
        #i'm thinking that we should just go ahead and start with a very high number and increment... lets say ten million
        #import pdb; pdb.set_trace()
        id_to_add = id_to_increment
        id_to_increment += 1
    return Player(id_to_add, data[0].text, data[1].text, data[2].text,data[3].text,data[4].text,data[5].text,data[6].text,data[7].text, team, year)

def create_url(args): 
    return "/".join(args)

def get_teams_by_conference_year(conference_data, teams_to_worry_about): 
    #example: "http://localhost:3000/teams/2009/Atlantic%20Coast%20Conference"
    conference_name = conference_data['name']
    conference_year = conference_data['year']
    url = create_url([method, host, 'teams', str(conference_year), conference_name])
    response = requests.get(url, headers={"accept": "application/json"}).json()[0]['teams']
    
    #now lets go ahead and structure the data in a easier to use way... plus the added intellisense of using an object
    for team in response: 
        teams_to_worry_about.append(DataHolder(team['name'],conference_year,conference_name,ids[team['name']]))

def get_conferences(year): 
    #example: http://localhost:3000/conferences/2009
    url = create_url([method, host, 'conferences', str(year)])
    result = requests.get(url, headers={"accept": "application/json"}).json()
    teams_to_worry_about = []
    for conference in result: 
        get_teams_by_conference_year(conference, teams_to_worry_about)
    
    return teams_to_worry_about

def handle_roster_by_year(year): 
    #first, we need to find a way to get the teams for the conference for the year
    teams_to_deal_with = get_conferences(year)
    
    #now that we have all of the teams for the given year, we can go ahead and get their players
    for team in teams_to_deal_with: 

        #example: http://www.cfbstats.com/2009/team/301/roster.html
        url = "http://www.cfbstats.com/{}/team/{}/roster.html".format(team.year, team.team_id)
        source = requests.get(url).text
        soup = BeautifulSoup(source, features="html.parser")

        #example: <table class="team-roster">
        table = soup.find("table", attrs={"class": "team-roster"})

        #now we need to extract all possible rows
        rows = table.find_all("tr")
        rows.pop(0)
        players = []
        for row in rows: 
            data = row.find_all("td")
            players.append(parse_player(data, team.conference, team.team_name, team.year))
        
        #now that we have the players for the team in the given year, we can format them and send them to the database through the API
        for player in players: 
            format_player_for_api_and_send(player)
            

        
for x in range(2009, 2020): 
    handle_roster_by_year(x)
    print(x, "done")