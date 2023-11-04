from flask import Flask, request, jsonify
from fantasy_tracker import create_league_conn, create_draft_df

app = Flask(__name__)

league = create_league_conn()

@app.route('/teams', methods=['GET'])
def get_teams():
    teams_df = create_teams_df(league)
    return teams_df.to_json(orient='records')

@app.route('/draft', methods=['GET'])
def get_draft():
    draft_df = create_draft_df(league)
    return draft_df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)