# Dependencies
import os
import pandas as pd
import zipfile
import sqlite3

# ---Step 1: download data from Kaggle---
# Download NFL draft data from Kaggle using below statement in terminal
# kaggle datasets download -d ulrikthygepedersen/nfl-draft-1985-2015

# Download NFL combine data Kaggle using below statement in terminal
# kaggle datasets download -d mitchellweg1/nfl-combine-results-dataset-2000-2022

# ---Step 2: extract NFL data---
# Extract NFL draft zip file
cur_folder = 'C:\\Bootcamp_Git\\project_4_healthcare\\NFL_data'
input_path = os.path.join(cur_folder, 'nfl-draft-1985-2015.zip')
with zipfile.ZipFile(input_path, 'r') as zip_ref:
    names = zip_ref.namelist()
    zip_ref.extractall(cur_folder)

#  Read into pandas dataframe and delete zip extract
zip_extract = os.path.join(cur_folder, names[0])
nfl_df = pd.read_csv(zip_extract)
os.remove(zip_extract)

# ---Step 3: extract combine data---
input_path = os.path.join(cur_folder, 'nfl-combine-results-dataset-2000-2022.zip')
with zipfile.ZipFile(input_path, 'r') as zip_ref:
    names = zip_ref.namelist()
    zip_ref.extractall(cur_folder)

# Read into pandas dataframe and delete zip extract
combine_df = pd.DataFrame()
for name in names:
    zip_extract = os.path.join(cur_folder, name)
    combine_files_df = pd.read_csv(zip_extract)
    combine_files_df['year'] = name[:4]
    combine_df = pd.concat([combine_df, combine_files_df], ignore_index=True)
    os.remove(zip_extract)

# ---Step 4: clean data---
# Remove unnecessary columns from dataframe
nfl_df = nfl_df[['player', 'year', 'rnd', 'pick', 'tm', 'pos', 'position_standard', 'college_univ']]

# Add player_id column to dataframe year + 4 character last name + 4 character first name because of same name for different players
nfl_df['player_id'] = nfl_df['year'].astype(str) + nfl_df['player'].str.split(' ').str[1].str.upper() + nfl_df['player'].str.split(' ').str[0].str.upper() + nfl_df['college_univ'].str[:3].str.upper()

# drop college_univ column
nfl_df.drop(['college_univ'], axis=1, inplace=True)

# Two players with same year, name, and college. Verified one player was not drafted. Remove not drafted player.
# drop records where player_id = '2012GRIFFINROBERTBAY' and pos = 'OL'
nfl_drop_index = nfl_df.loc[(nfl_df['player_id'] == '2012GRIFFINROBERTBAY') & (nfl_df['pos'] == 'OL')].index
nfl_df.drop(nfl_drop_index, inplace=True)

# rename Ht column to height
combine_df.rename(columns={'Ht': 'height'}, inplace=True)

# split Ht column into two columns height and inches and convert height from feet to inches and add inches column to height column
combine_df[['ht', 'in']] = combine_df['height'].str.split('-', expand=True)
combine_df['in'].fillna(0, inplace=True)
combine_df['ht'].fillna(0, inplace=True)
combine_df['ht'] = combine_df['ht'].astype(int) * 12
combine_df['ht'] = combine_df['ht'] + combine_df['in'].astype(int)

# drop inches columns
combine_df.drop(['in'], axis=1, inplace=True)

# Replace '-' with ' ft ' in 'Ht' column and add ' in' to end of 'Ht' column for Tableau dashboard
combine_df['height'] = combine_df['height'].str.replace('-', ' ft ')
combine_df['height'] = combine_df['height'] + ' in'

# Add player_id column to dataframe year + 4 character last name + 4 character first name because of same name for different players
combine_df['player_id'] = combine_df['year'].astype(str) + combine_df['Player'].str.split(' ').str[1].str.upper() + combine_df['Player'].str.split(' ').str[0].str.upper()  + combine_df['School'].str[:3].str.upper()

# drop records where player_id = '2007DAVISBUSTERFLO' and pos = 'WR'
combine_drop_index = combine_df.loc[(combine_df['player_id'] == '2007DAVISBUSTERFLO') & (combine_df['Pos'] == 'WR')].index
combine_df.drop(combine_drop_index, inplace=True)

# drop records where player_id = '2005JOHNSONDERRICKTEX' and pos = 'CB'
combine_drop_index = combine_df.loc[(combine_df['player_id'] == '2005JOHNSONDERRICKTEX') & (combine_df['Pos'] == 'CB')].index
combine_df.drop(combine_drop_index, inplace=True)


# Merge dataframes on player_id
draft_df = combine_df.merge(nfl_df, on=['player_id'], how='left')

# Drop fields player_name_y and year_y
draft_df.drop(['player', 'year_y'], axis=1, inplace=True)

# Rename fields
draft_df.rename(columns={'Player': 'player_name', 'Pos': 'position_combine', 'year_x': 'year', 'pos': 'position_nfl',
                         'position_standard': 'position_nfl_std', 'tm': 'nfl_team', 'Wt': 'weight', '40yd': 'forty_yard',
                         'Vertical': 'vertical_leap', 'Bench': 'bench_press', 'Broad Jump': 'broad_jump', 'Shuttle': 'shuttle_run',
                         '3Cone': 'three_cone', 'rnd': 'draft_round', 'pick': 'draft_pick'}, inplace=True)

# Reorder columns
draft_df = draft_df[['player_id', 'player_name', 'year', 'School', 'position_combine', 'height', 'ht', 'weight', 'forty_yard',
                     'vertical_leap', 'bench_press', 'broad_jump', 'three_cone', 'shuttle_run', 'draft_round', 'draft_pick',
                      'nfl_team', 'position_nfl', 'position_nfl_std']]

# ---Step 6: Limit data and fillna---
# drop records where draft_round = NaN
# draft_df = draft_df[draft_df['draft_round'].notna()]

# round forty_yard to 2 decimal places
draft_df['forty_yard'] = draft_df['forty_yard'].round(2)

# create list of positions to include in dashboard
pos_list = ['C', 'CB', 'DE', 'DT', 'FB', 'ILB', 'K', 'LS', 'OG', 'OLB', 'OT', 'P', 'QB', 'RB', 'S', 'TE', 'WR']

# add column for bench_press if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['bench_press'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['bench_press_score'] = 0
        event_df.loc[event_df['bench_press'] >= event_df['bench_press'].quantile(.75), 'bench_press_score'] = 4
        event_df.loc[(event_df['bench_press'] >= event_df['bench_press'].median()) & (event_df['bench_press'] < event_df['bench_press'].quantile(.75)), 'bench_press_score'] = 3
        event_df.loc[(event_df['bench_press'] >= event_df['bench_press'].quantile(.25)) & (event_df['bench_press'] < event_df['bench_press'].median()), 'bench_press_score'] = 2
        event_df.loc[event_df['bench_press'] < event_df['bench_press'].quantile(.25), 'bench_press_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)


draft_df = draft_df.merge(event_combined_df[['player_id', 'bench_press_score']], on=['player_id'], how='left')

# add column for broad_jump if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['broad_jump'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['broad_jump_score'] = 0
        event_df.loc[event_df['broad_jump'] >= event_df['broad_jump'].quantile(.75), 'broad_jump_score'] = 4
        event_df.loc[(event_df['broad_jump'] >= event_df['broad_jump'].median()) & (event_df['broad_jump'] < event_df['broad_jump'].quantile(.75)), 'broad_jump_score'] = 3
        event_df.loc[(event_df['broad_jump'] >= event_df['broad_jump'].quantile(.25)) & (event_df['broad_jump'] < event_df['broad_jump'].median()), 'broad_jump_score'] = 2
        event_df.loc[event_df['broad_jump'] < event_df['broad_jump'].quantile(.25), 'broad_jump_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)

draft_df = draft_df.merge(event_combined_df[['player_id', 'broad_jump_score']], on=['player_id'], how='left')

# add column for forty_yard if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['forty_yard'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['forty_yard_score'] = 0
        event_df.loc[event_df['forty_yard'] <= event_df['forty_yard'].quantile(.25), 'forty_yard_score'] = 4
        event_df.loc[(event_df['forty_yard'] <= event_df['forty_yard'].median()) & (event_df['forty_yard'] > event_df['forty_yard'].quantile(.25)), 'forty_yard_score'] = 3
        event_df.loc[(event_df['forty_yard'] <= event_df['forty_yard'].quantile(.75)) & (event_df['forty_yard'] > event_df['forty_yard'].median()), 'forty_yard_score'] = 2
        event_df.loc[event_df['forty_yard'] > event_df['forty_yard'].quantile(.75), 'forty_yard_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)

draft_df = draft_df.merge(event_combined_df[['player_id', 'forty_yard_score']], on=['player_id'], how='left')

# add column for shuttle_run if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['shuttle_run'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['shuttle_run_score'] = 0
        event_df.loc[event_df['shuttle_run'] <= event_df['shuttle_run'].quantile(.25), 'shuttle_run_score'] = 4
        event_df.loc[(event_df['shuttle_run'] <= event_df['shuttle_run'].median()) & (event_df['shuttle_run'] > event_df['shuttle_run'].quantile(.25)), 'shuttle_run_score'] = 3
        event_df.loc[(event_df['shuttle_run'] <= event_df['shuttle_run'].quantile(.75)) & (event_df['shuttle_run'] > event_df['shuttle_run'].median()), 'shuttle_run_score'] = 2
        event_df.loc[event_df['shuttle_run'] > event_df['shuttle_run'].quantile(.75), 'shuttle_run_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)

draft_df = draft_df.merge(event_combined_df[['player_id', 'shuttle_run_score']], on=['player_id'], how='left')

# add column for three_cone if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['three_cone'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['three_cone_score'] = 0
        event_df.loc[event_df['three_cone'] <= event_df['three_cone'].quantile(.25), 'three_cone_score'] = 4
        event_df.loc[(event_df['three_cone'] <= event_df['three_cone'].median()) & (event_df['three_cone'] > event_df['three_cone'].quantile(.25)), 'three_cone_score'] = 3
        event_df.loc[(event_df['three_cone'] <= event_df['three_cone'].quantile(.75)) & (event_df['three_cone'] > event_df['three_cone'].median()), 'three_cone_score'] = 2
        event_df.loc[event_df['three_cone'] > event_df['three_cone'].quantile(.75), 'three_cone_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)

draft_df = draft_df.merge(event_combined_df[['player_id', 'three_cone_score']], on=['player_id'], how='left')

# add column for vertical_leap if >= 3rd quartile = 4 elseif >= median elseif >=  1st quartile = 2 else = 1 do not include NaN
event_combined_df = pd.DataFrame()
for pos in pos_list:
    event_df = draft_df[(draft_df['vertical_leap'].notna()) & (draft_df['position_combine'] == pos)].copy()
    if len(event_df) == 0:
        pass
    else:
        event_df['vertical_leap_score'] = 0
        event_df.loc[event_df['vertical_leap'] >= event_df['vertical_leap'].quantile(.75), 'vertical_leap_score'] = 4
        event_df.loc[(event_df['vertical_leap'] >= event_df['vertical_leap'].median()) & (event_df['vertical_leap'] < event_df['vertical_leap'].quantile(.75)), 'vertical_leap_score'] = 3
        event_df.loc[(event_df['vertical_leap'] >= event_df['vertical_leap'].quantile(.25)) & (event_df['vertical_leap'] < event_df['vertical_leap'].median()), 'vertical_leap_score'] = 2
        event_df.loc[event_df['vertical_leap'] < event_df['vertical_leap'].quantile(.25), 'vertical_leap_score'] = 1
        event_combined_df = pd.concat([event_combined_df, event_df], ignore_index=True)

draft_df = draft_df.merge(event_combined_df[['player_id', 'vertical_leap_score']], on=['player_id'], how='left')


# # fill NaN with 0
# draft_df['bench_press_score'].fillna(0, inplace=True)
# draft_df['broad_jump_score'].fillna(0, inplace=True)
# draft_df['forty_yard_score'].fillna(0, inplace=True)
# draft_df['shuttle_run_score'].fillna(0, inplace=True)
# draft_df['three_cone_score'].fillna(0, inplace=True)
# draft_df['vertical_leap_score'].fillna(0, inplace=True)

# add column for bench_press_score + broad_jump_score + forty_yard_score + shuttle_run_score + three_cone_score + vertical_leap_score
draft_df['combine_score'] = draft_df['bench_press_score'] + draft_df['broad_jump_score'] + draft_df['forty_yard_score'] + draft_df['shuttle_run_score'] + draft_df['three_cone_score'] + draft_df['vertical_leap_score']

# add column if draft_pick is NaN = 0 else = 1
draft_df['draft_pick_flag'] = 0
draft_df.loc[draft_df['draft_pick'].notna(), 'draft_pick_flag'] = 1

# Convert year to int
draft_df['year'] = draft_df['year'].astype(int)

# Limit to years 2000-2015
draft_df = draft_df.loc[(draft_df['year'] >= 2000) & (draft_df['year'] <= 2015)]

# write df to sqlite
conn = sqlite3.connect('Resources/database.db')
draft_df.to_sql('players_raw', conn, if_exists='replace', index=False)

# for column vertical_leap, bench_press, broad_jump, shuttle_run, three_cone replace NaN with the median of the column based on position_combine and draft_pick_flag = 1
draft_df['vertical_leap'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['vertical_leap'].transform(lambda x: x.fillna(x.median()))
draft_df['bench_press'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['bench_press'].transform(lambda x: x.fillna(x.median()))
draft_df['broad_jump'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['broad_jump'].transform(lambda x: x.fillna(x.median()))
draft_df['shuttle_run'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['shuttle_run'].transform(lambda x: x.fillna(x.median()))
draft_df['three_cone'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['three_cone'].transform(lambda x: x.fillna(x.median()))
draft_df['forty_yard'] = draft_df.groupby(['position_combine', 'draft_pick_flag'])['forty_yard'].transform(lambda x: x.fillna(x.median()))

# for column shuttle_run and three_cone replace NaN with the median of the column because kicker and punter did not have scores
# to populate based on position_combine
draft_df['shuttle_run'] = draft_df['shuttle_run'].fillna(draft_df['shuttle_run'].median())
draft_df['three_cone'] = draft_df['three_cone'].fillna(draft_df['three_cone'].median())

# ---Step 7: output data---
# write draft_df to csv
draft_df.to_csv('Resources/draft_sqlite_data.csv', index=False)

# write df to sqlite
draft_df.to_sql('players', conn, if_exists='replace', index=False)

conn.close()

exit()