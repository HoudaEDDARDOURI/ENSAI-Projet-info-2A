from dao.db_connection import DBConnection

# Récupère la connexion
conn = DBConnection().connection




with conn.cursor() as cur:
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'app';
    """)
    print(cur.fetchall())

