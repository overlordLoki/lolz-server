import pandas as pd
import database as db

# fuction to make data frame of the teams and ranking tear for a tournament
def rankingDF(df_tournament):
    tournament_name = df_tournament['tournament_name'][0]
    df_teams = db.getTeamNames(tournament_name)
    df = pd.DataFrame(columns=['team_name','rank','tournament_name'])

    return df

