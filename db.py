import sqlite3
import json

def db_init():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS diets (user_id INTEGER, dietaryPreference TEXT, healthGoal TEXT, numDays INTEGER, allergies TEXT, budgetConstraint INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS diets_plan (user_id INTEGER, text TEXT, dayNum INTEGER)")
    conn.commit()
    conn.close()
db_init()

class Db():
    def insert_to_diets(self, data):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("INSERT INTO diets VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
    def check_if_already_exists(self, user_id):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM diets WHERE user_id=?", (user_id,))
        r = c.fetchone()
        conn.commit()
        conn.close()
        print(r[0])
        if r[0] == 0:
            return False
        else:
            return True

    def get_data_by_userid(self, user_id):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM diets WHERE user_id=?", (user_id,))
        r = c.fetchone()
        conn.commit()
        conn.close()
        print(r)
        data = dict()
        data['user'] = r[0]
        data['dietaryPreference'] = r[1]
        data['healthGoal'] = r[2]
        data['numDays'] = r[3]
        data['allergies'] = list(r[4])
        data['budgetConstraint'] = r[5]
        rJson = json.dumps(data)
        return rJson

    def insert_diets_plan(self, data):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("INSERT INTO diets_plan VALUES (?,?,?)", data)
        conn.commit()
        conn.close()

    def get_diets_plan_by_day(self, user_id, dayNum):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM diets_plan WHERE user_id = ? AND dayNum= ?", (user_id, dayNum))
        r = c.fetchone()
        conn.commit()
        conn.close()
        if r == None:
            return False
        else:
            return r



db = Db()