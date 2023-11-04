'''
Server python file that uses flask to connect to the fantasy_tracker app
and build an api out of the functions built in fantasy_tracker.py
'''
from flask import Flask, request, jsonify
from fantasy_tracker import create_league_conn, create_draft_df, create_teams_df
import pandas as pd

app = Flask(__name__)

league = create_league_conn()

@app.route('/teams', methods=['GET'])
def get_teams():
    teams_df = create_teams_df(league)
    return teams_df.to_json()

@app.route('/team/<teamname>', methods=['GET'])
def get_team(teamname):
    selected_team = teamname.lower()
    teams_df = create_teams_df(league)
    return teams_df.loc[teams_df['Team_Names']== selected_team, 'Roster'].to_json()

@app.route('/draft', methods=['GET'])
def get_draft():
    draft_df = create_draft_df(league)
    return draft_df.to_json()

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}, 404)

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}, 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)