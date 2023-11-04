'''
Main python file used to connect to fantasy football league and pull stats
'''
from espn_api.football import League
import pandas as pd
import os
from dotenv import load_dotenv

# Load in environment variables to access league
load_dotenv()
ESPNS2 = os.environ.get('ESPNS2')
SWID = os.environ.get('SWID')
LEAGUEID = os.environ.get('LEAGUEID')

# Create league connection
league = League(league_id=LEAGUEID, year=2023, espn_s2=ESPNS2, swid=SWID)

# league.draft
# https://github.com/cwendt94/espn-api/wiki/Football-Intro

print(league.draft)