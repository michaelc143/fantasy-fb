from espn_api.football import League
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

ESPNS2 = os.environ.get('ESPNS2')
SWID = os.environ.get('SWID')
LEAGUEID = os.environ.get('LEAGUEID')

league = League(league_id=LEAGUEID, year=2023, espn_s2=ESPNS2, swid=SWID)
# league.draft
# https://github.com/cwendt94/espn-api/wiki/Football-Intro
print(league.draft)