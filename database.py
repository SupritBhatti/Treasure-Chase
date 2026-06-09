import sqlite3
con = sqlite3.connect("treasureChase_data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS high_scores(score INT)")
cur.execute("CREATE TABLE IF NOT EXISTS coin_total(coins INT)")
cur.execute("CREATE TABLE IF NOT EXISTS player_data(weapon TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS owned_weapons (weapon TEXT UNIQUE)")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def insert_score(score):
    cur.execute("INSERT INTO high_scores (score) VALUES (?)", (score,))
    con.commit()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def insert_coins(coins):
    cur.execute("INSERT INTO coin_total (coins) VALUES (?)", (coins,))
    con.commit()

def get_coin_total():
    cur.execute("SELECT SUM(coins) FROM coin_total")
    total_coins = cur.fetchone()[0]
    if total_coins is None:
        total_coins = 0
    return total_coins

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def set_weapon(weapon_name):
    cur.execute("DELETE FROM player_data")  # Clear previous selection
    cur.execute("INSERT INTO player_data (weapon) VALUES (?)", (weapon_name,))
    con.commit()

def get_weapon():
    cur.execute("SELECT weapon FROM player_data")
    result = cur.fetchone()
    return result[0] if result else "Start"  # Default to "Start" if no value is stored

def purchase_weapon(weapon_name):
    #stores purchased weapon into database
    cur.execute("INSERT OR IGNORE INTO owned_weapons (weapon) VALUES (?)", (weapon_name,))

def has_weapon(weapon_name):
    #checks if weapon is already purchased
    cur.execute("SELECT weapon FROM owned_weapons WHERE weapon = ?", (weapon_name,))
    return cur.fetchone() is not None  # Returns True if the weapon is owned, False otherwise
