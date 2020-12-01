import psycopg2


class Database():

    def __init__(self, database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.con = None
        self.cursor = None

    def connect(self):
        try:
            self.con = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="postgres",
                host="127.0.0.1",
                port="5432"  
        )
            self.cursor = self.con.cursor()
            return 0
        except (Exception, psycopg2.Error):
            return -1

    def create_table_players(self, table_name):
        self.cursor.execute("select exists(select * from information_schema.tables where table_name ='{}')".format(table_name.lower()))
        z = self.cursor.fetchone()[0]
        if not bool(z):
            create_table_query = '''CREATE TABLE {}
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            ROLE           TEXT    NOT NULL,
            COUNTRY        TEXT    NOT NULL, 
            NUMBER         INT NOT NULL); '''.format(table_name.lower())
            self.cursor.execute(create_table_query)
            self.con.commit()
            return("Table created")
        else:
            return("Table already exist")


    def insert_player(self, data):
        postgres_insert_query = """ INSERT INTO players (ID, NAME, ROLE, COUNTRY, NUMBER) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = data
        self.cursor.execute(postgres_insert_query, record_to_insert)
        self.con.commit()

    def read_player(self, id):
        postgreSQL_select_Query = "select * from players where id = %s"
        self.cursor.execute(postgreSQL_select_Query, (id,))
        player_records = self.cursor.fetchall()
        return player_records

    def close_db_connection(self):
        if self.con:
            self.cursor.close()
            self.con.close()
