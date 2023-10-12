# Dependencies
import os
import pandas as pd
import zipfile

# Download NFL draft data from Kaggle using below statement in terminal
# kaggle datasets download -d ulrikthygepedersen/nfl-draft-1985-2015

# Download NFL combine data Kaggle using below statement in terminal
# kaggle datasets download -d mitchellweg1/nfl-combine-results-dataset-2000-2022

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

# Remove unnecessary columns from dataframe
nfl_df = nfl_df[['player', 'year', 'rnd', 'pick', 'tm', 'pos', 'position_standard']]

# Rename columns for Tableau dashboard
nfl_df.rename(columns={'player': 'player_name', 'rnd': 'draft_round', 'pick': 'draft_pick', 'tm': 'team', 'pos': 'position'}, inplace=True)

# Limit to years 2000-2015
nfl_df = nfl_df.loc[(nfl_df['year'] >= 2000) & (nfl_df['year'] <= 2015)]

# Remove NaN values from dataframe
# nfl_clean_df = nfl_df.dropna()
nfl_clean_df = nfl_df.copy()

# Add player_id column to dataframe year + 4 character last name + 4 character first name because of same name for different players
nfl_clean_df['player_id'] = nfl_clean_df['year'].astype(str) + nfl_clean_df['player_name'].str[:4] + nfl_clean_df['player_name'].str.split(' ').str[1].str[:4]

# Extract NFL combine zip files
input_path = os.path.join(cur_folder, 'nfl-combine-results-dataset-2000-2022.zip')
with zipfile.ZipFile(input_path, 'r') as zip_ref:
    names = zip_ref.namelist()
    zip_ref.extractall(cur_folder)

# Read into pandas dataframe and delete zip extract
combine_df = pd.DataFrame()
for name in names:
    zip_extract = os.path.join(cur_folder, name)
    nfl_df = pd.read_csv(zip_extract)
    nfl_df['year'] = name[:4]
    combine_df = pd.concat([combine_df, nfl_df], ignore_index=True)
    os.remove(zip_extract)

# Convert year to int
nfl_df['year'] = nfl_df['year'].astype(int)

# Replace '-' with ' ft ' in 'Ht' column
combine_df['Ht'] = combine_df['Ht'].str.replace('-', ' ft ')

# Add ' in' to end of 'Ht' column
combine_df['Ht'] = combine_df['Ht'] + ' in'

# Rename columns for Tableau dashboard
combine_df.rename(columns={'Ht': 'height', 'Wt': 'weight', '40yd': 'forty_yard', 'Vertical': 'vertical_leap', 'Bench': 'bench_press', 'Broad Jump': 'broad_jump',
                           'Shuttle': 'shuttle_run', '3Cone': 'three_cone', 'Player': 'player_name', 'Pos': 'position'}, inplace=True)

# Add player_id column to dataframe year + 4 character last name + 4 character first name because of same name for different players
combine_df['player_id'] = combine_df['year'].astype(str) + combine_df['player_name'].str[:4] + combine_df['player_name'].str.split(' ').str[1].str[:4]

# Remove NaN values from dataframe
# combine_clean_df = combine_df.dropna()
combine_clean_df = combine_df.copy()

# Drop record where player_name = 'Malcolm Brown' because of two players with Malcolm and Malcom Brown name
combine_clean_df = combine_clean_df[combine_clean_df['player_name'] != 'Malcolm Brown']

# Merge dataframes on player_id
draft_df = combine_clean_df.merge(nfl_clean_df, on=['player_id'], how='left')

# Drop fields player_name_y and year_y
draft_df.drop(['player_name_y', 'year_y'], axis=1, inplace=True)

# Rename fields
draft_df.rename(columns={'player_name_x': 'player_name', 'position_x': 'position_combine', 'year_x': 'year',
                         'position_y': 'position_nfl', 'position_standard': 'position_nfl_standard', 'team': 'nfl_team'}, inplace=True)

# Reorder columns
draft_df = draft_df[['player_id', 'year', 'player_name', 'position_combine', 'School','height', 'weight', 'forty_yard', 'vertical_leap', 
                     'bench_press', 'broad_jump', 'three_cone', 'shuttle_run', 'nfl_team', 'position_nfl', 'position_nfl_standard', 'draft_round', 'draft_pick']]

# Remove NaN values from dataframe
# draft_df = draft_df.dropna()
draft_v02_df = draft_df.copy()

# write df to csv
draft_v02_df.to_csv('C:\\Bootcamp_Git\\project_4_healthcare\\NFL_data\\draft_df.csv', index=False)
