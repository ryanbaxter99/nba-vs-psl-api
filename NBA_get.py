import requests
import sqlite3
import os
import json
import time
import pprint
import time


'''
balldontlie API
Documentation --> https://www.balldontlie.io/#introduction
No API key required
Rate Limit is 60 Per Minute 
'''

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in this function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def  createPositionTable():
    ''' 
    Creates a table of all of the players from the current NBA roster by their position
    Output is the table
    Max of 25 players are added per time as we limit the amount of games per API request to 25
    '''

    cur, conn = setUpDatabase('sports.db')
    cur.execute('CREATE TABLE IF NOT EXISTS IDs (id INTEGER PRIMARY KEY, NBA_id INTEGER UNIQUE, position INTEGER)')
    url = 'https://www.balldontlie.io/api/v1/players'
    
    count = 0

    for i in range(1, 38):
        querystring = {"per_page":"100", "page":str(i)}
        r = requests.get(url, params=querystring)
        data = r.text
        dict_list = json.loads(data)['data']
        
        for player in dict_list:
            # get the players team position
            player_position = player["position"]
            if player_position is None or "":
                continue

            height_ft = player["height_feet"]
            height_inch = player["height_inches"]

            if height_ft is None and height_inch is None:
                continue 
            
            # convert the position into ints
            if player_position == 'G':
                player_position = 3
            elif player_position == 'C':
                player_position = 2
            elif player_position == 'F':
                player_position = 1
            else:
                player_position = 0

            NBA_id = player['id']

            id_in_data = cur.execute('SELECT NBA_id FROM IDs WHERE NBA_id = ?', (NBA_id,)).fetchone()

            if id_in_data is None:
                cur.execute('INSERT OR IGNORE INTO IDs (NBA_id, position) VALUES (?, ?)', (NBA_id, player_position))
               
                conn.commit()
                count += 1
                if count == 25:
                    print(f'Added {count} NBA players to IDs Table')
                    total = cur.execute('SELECT MAX(id) FROM IDs').fetchone()[0]
                    print(f'{total} total players in IDs Table')
                    return
    cur.close()

def createHeightTable():
    ''' 
    Creates a table of all of the players from the current NBA roster by their height
    Output is the table
    Max of 25 players are added per time as we limit the amount of games per API request to 25
    '''
    cur, conn = setUpDatabase('sports.db')
    cur.execute('CREATE TABLE IF NOT EXISTS PlayerHeight (id INTEGER PRIMARY KEY, NBA_id INTEGER UNIQUE, height INTEGER)')
    url = 'https://www.balldontlie.io/api/v1/players'

    temp = 0
    for i in range(1, 38):
        query = {"per_page":"100", "page":str(i)}
        r = requests.get(url, params=query)
        data = r.text
        in_data = json.loads(data)['data']

        for player in in_data:
            height_ft = player["height_feet"]
            height_inch = player["height_inches"]

            if height_ft is None or height_inch is None:
                continue 

            height_ft = int(height_ft)
            height_inch = int(height_inch)
            player_height = (height_ft * 12) + height_inch

            NBA_id = player['id']
            id_in_data = cur.execute('SELECT NBA_id FROM PlayerHeight WHERE NBA_id = ?', (NBA_id,)).fetchone()

            if id_in_data is None:
                cur.execute('INSERT OR IGNORE INTO PlayerHeight (NBA_id, height) VALUES (?, ?)', (NBA_id, player_height))
                
                conn.commit()
                temp += 1
                if temp == 25:
                    print(f'Added {temp} NBA players to PlayerHeight Table')
                    total = cur.execute('SELECT MAX(id) FROM PlayerHeight').fetchone()[0]
                    print(f'{total} total players in PlayerHeight Table')
                    print('Need to wait 30 seconds before running NBA api again')
                    return 
    cur.close()

if __name__ == '__main__':
    createPositionTable()
    createHeightTable()
    