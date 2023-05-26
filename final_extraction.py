import pandas as pd

df = pd.read_csv('basketball_titles.csv')


def get_entities():
    df_timelines = df.sort_values(by=['total_timelines'])[-3000:]
    df_keys = df_timelines.sort_values(by=['total_keys'])[-2000:]
    df_revisions = df_keys.sort_values(by=['revisions'])[-1000:]
    df_revisions['Name'].to_csv('basketball_players.txt', index=False)


get_entities()