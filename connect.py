import os, sqlite3

root = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(root, "nutrition.db")
conn = sqlite3.connect(db)
cur = conn.cursor()
