from flask import Flask
from flask import request
import requests


app = Flask(__name__)

api_key = 'RGAPI-865b0221-eb73-41c6-9900-8bab2382f96a'


@app.route('/lastGame', methods=['GET'])
def main():
    puuid = _get_puuid_by_name()

    last_games = _get_matches(puuid)

    last_game = last_games[0] 

    return _get_match_members(last_game)

def _get_puuid_by_name():
    name = request.args.get('name')

    base_url = 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'

    response = requests.get(base_url+name, headers={"X-Riot-Token": api_key}).json()

    return response['puuid']

def _get_matches(puuid):
    base_url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/'

    response = requests.get(base_url+puuid+'/ids?start=0&count=20', headers={"X-Riot-Token": api_key}).json()

    return response

def _get_match_members(game_id):
    base_url = 'https://europe.api.riotgames.com/lol/match/v5/matches/'

    response = requests.get(base_url+game_id, headers={"X-Riot-Token": api_key}).json()

    team_1 = {}
    team_2 = {}

    for participant in response["info"]["participants"]:
        summoner_name = participant["summonerName"]
        champion_name = participant["championName"]
        team_id = participant["teamId"]

        if team_id == 100:
            team_1[summoner_name] = champion_name        
        elif team_id == 200:
            team_2[summoner_name] = champion_name

    team_results = {}

    team_results["team_1"] = team_1
    team_results["team_2"] = team_2

    return team_results


app.run()