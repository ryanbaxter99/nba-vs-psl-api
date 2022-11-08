import requests 
import secrets
import sqlite3
import os
import json
import time 
from bs4 import BeautifulSoup


'''
API-FOOTBALL
Documentation = https://www.api-football.com/documentation-v3#section/Introduction
Needs API key.
Only allowed 100 requests per day (30 per minute).
'''

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "5eca74bf8bmsh6463613242d8822p10f390jsn03d55af04856"
}

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in this function to update databses.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def player_table():
    '''
    Creates a table with players from the Premier Soccer League in the 2020 season.
    - player_id is the id of that player given by the API.
    - player_height is the height of the player in cm.
    - player_posiiton is a number that correlates to the players position
    - - 0 = attacker, 1 = midfielder, 2 = defender, 3 = goalkeeper
    '''
    cur, conn = setUpDatabase('sports.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Premier_League (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, height INTEGER , position INTEGER)')

    count = 0
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    
    for i in range(1, 34):
        querystring = {"league":"39","season":"2020","page":str(i)}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.text
        dict_list = json.loads(data)['response']

        for player in dict_list:
            player_height = player['player']['height']
            
            if player_height is None:
                continue

            player_height = player_height.replace('cm', '')
           
            player_height = int(player_height)
            #convert height from cm to inches
            player_height = (player_height / 2.54)
            
            player_position = player['statistics'][0]['games']['position']
            
            if player_position == 'Attacker':
                player_position = 0
            elif player_position == 'Midfielder':
                player_position = 1
            elif player_position == 'Defender':
                player_position = 2
            else:
                player_position = 3

            player_appearence = player['statistics'][0]['games']['appearences']
            if player_appearence is None:
                continue

            player_id = player['player']['id']
            id_in_data = cur.execute('SELECT player_id FROM Premier_League WHERE player_id = ?', (player_id,)).fetchone()

            if id_in_data is None and player_appearence >= 10:
                cur.execute('INSERT OR IGNORE INTO Premier_League (player_id, height, position) VALUES (?, ?, ?)', (player_id, player_height, player_position))
               
                conn.commit()
                count += 1
                if count == 25:
                    print(f'Added {count} players to table')
                    total = cur.execute('SELECT MAX(id) FROM Premier_League').fetchone()[0]
                    print(f'{total} total players')
                    print('Need to wait 30 seconds before running Premier_League api again')
                    return 


if __name__ == '__main__':
    player_table()
    
