'''
Main python file used to connect to fantasy football league and pull stats
'''
from espn_api.football import League
import pandas as pd
import os
from dotenv import load_dotenv

def create_league_conn():
    # Load in environment variables to access league
    load_dotenv()
    ESPNS2 = os.environ.get('ESPNS2')
    SWID = os.environ.get('SWID')
    LEAGUEID = os.environ.get('LEAGUEID')
    # Create league connection
    league = League(league_id=LEAGUEID, year=2023, espn_s2=ESPNS2, swid=SWID)
    return league

# league.draft
# https://github.com/cwendt94/espn-api/wiki/Football-Intro

def create_teams_df(league):
    team_names = []
    division_names = []
    rosters = []
    schedules = []
    standings = []
    best_players = []
    for team in league.teams:
        team_names.append(team.team_name)
        division_names.append(team.division_name)
        rosters.append(team.roster)
        schedules.append(team.schedule)
        standings.append(int(team.standing))
    for roster in rosters:
        best_player = roster[0]
        for player in roster:
            if player.total_points > best_player.total_points:
                best_player = player
        best_players.append(best_player)
    teams = pd.DataFrame()
    teams['Team_Names'] = team_names
    teams['Division'] = division_names
    # teams['Schedule'] = schedules
    teams['Ranking'] = standings
    teams = teams.sort_values(by='Ranking')
    return teams

def create_draft_df(league):
    team_names = []
    draft_picks = {}
    for team in league.teams:
        team_names.append(team.team_name)
    for team in team_names:
        draft_picks[team] = []
    draft = league.draft
    for pick in draft:
        draft_picks[pick.team.team_name].append(pick.playerName)
    teams = pd.DataFrame()
    teams['Team_Names'] = team_names
    teams['Draft_Picks'] = [draft_picks.get(team, []) for team in teams['Team_Names']]
    return teams