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
    roster_df = []
    for team in league.teams:
        team_names.append(team.team_name)
        division_names.append(team.division_name)
        rosters.append(team.roster)
        schedules.append(team.schedule)
        standings.append(int(team.standing))
    final_team_names = []
    for team_name in team_names:
        under_name = team_name.replace(" ", "_")
        final_team_names.append(under_name.lower())
    for roster in rosters:
        # best_player = roster[0]
        # for player in roster:
        #     if player.total_points > best_player.total_points:
        #         best_player = player
        # best_players.append(best_player)
        temp_roster = []
        for player in roster:
            temp_roster.append(player.name)
        roster_df.append(temp_roster)
    teams = pd.DataFrame()
    teams['Team_Names'] = final_team_names
    teams['Division'] = division_names
    # teams['Schedule'] = schedules
    teams['Ranking'] = standings
    teams['Roster'] = roster_df
    teams = teams.sort_values(by='Ranking')
    return teams

def create_draft_df(league):
    team_names = []
    draft_picks = {}
    rosters = []
    best_players = []
    impact_players = []
    for team in league.teams:
        team_names.append(team.team_name)
        rosters.append(team.roster)
    for roster in rosters:
        best_player = roster[0]
        big_impact = roster[0]
        for player in roster:
            if player.avg_points > best_player.avg_points:
                best_player = player
            if (player.avg_points - player.projected_avg_points) > (big_impact.avg_points - big_impact.projected_avg_points):
                big_impact = player
        best_players.append(("Name: " + best_player.name[:10], "Avg Points: " + str(best_player.avg_points)))
        impact_players.append(("Name: " + big_impact.name[:10], "Pt Differential: " + str(int(big_impact.avg_points - big_impact.projected_avg_points))))
    for team in team_names:
        draft_picks[team] = []
    draft = league.draft
    for pick in draft:
        draft_picks[pick.team.team_name].append(pick.playerName)
    teams = pd.DataFrame()
    teams['Team_Names'] = team_names
    teams['Draft_Picks'] = [draft_picks.get(team, []) for team in teams['Team_Names']]
    teams['Best_Player'] = best_players
    teams['Impact_Player'] = impact_players
    return teams
