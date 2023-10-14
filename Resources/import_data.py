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
nfl_df = nfl_df[['player', 'year', 'rnd', 'pick', 'tm', 'pos', 'position_standard']]

# Convert year to int
nfl_df['year'] = nfl_df['year'].astype(int)

# Limit to years 2000-2015
nfl_df = nfl_df.loc[(nfl_df['year'] >= 2000) & (nfl_df['year'] <= 2015)]

# Add player_id column to dataframe year + 4 character last name + 4 character first name because of same name for different players
nfl_df['player_id'] = nfl_df['year'].astype(str) + nfl_df['player'].str[:4] + nfl_df['player'].str.split(' ').str[1].str[:4]

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
combine_df['player_id'] = combine_df['year'].astype(str) + combine_df['Player'].str[:4] + combine_df['Player'].str.split(' ').str[1].str[:4]

# Drop record where player_name = 'Malcolm Brown' because of two players with Malcolm and Malcom Brown name
combine_df = combine_df[combine_df['Player'] != 'Malcolm Brown']

# ---Step 5: combine data---
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
draft_df = draft_df[draft_df['draft_round'].notna()]

# for column vertical_leap, bench_press, broad_jump, shuttle_run, three_cone replace NaN with the median of the column based on position_combine
draft_df['forty_yard'] = draft_df.groupby('position_combine')['forty_yard'].transform(lambda x: x.fillna(x.median()))
draft_df['vertical_leap'] = draft_df.groupby('position_combine')['vertical_leap'].transform(lambda x: x.fillna(x.median()))
draft_df['bench_press'] = draft_df.groupby('position_combine')['bench_press'].transform(lambda x: x.fillna(x.median()))
draft_df['broad_jump'] = draft_df.groupby('position_combine')['broad_jump'].transform(lambda x: x.fillna(x.median()))
draft_df['shuttle_run'] = draft_df.groupby('position_combine')['shuttle_run'].transform(lambda x: x.fillna(x.median()))
draft_df['three_cone'] = draft_df.groupby('position_combine')['three_cone'].transform(lambda x: x.fillna(x.median()))

# for column shuttle_run and three_cone replace NaN with the median of the column because kicker and punter did not have scores
# to populate based on position_combine
draft_df['shuttle_run'] = draft_df['shuttle_run'].fillna(draft_df['shuttle_run'].median())
draft_df['three_cone'] = draft_df['three_cone'].fillna(draft_df['three_cone'].median())

# round forty_yard to 2 decimal places
draft_df['forty_yard'] = draft_df['forty_yard'].round(2)

# ---Step 7: output data---
# write draft_df to csv
draft_df.to_csv('Resources/draft_sqlite_data.csv', index=False)

# write df to sqlite
conn = sqlite3.connect('Resources/database.db')
draft_df.to_sql('players', conn, if_exists='replace', index=False)

conn.close()

exit()