import sqlite3

CONN = sqlite3.connect('./music.db')
CURSOR = CONN.cursor()

class Song:

    all = []

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        with CONN:
            CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs
        """
        with CONN:
            CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """
        with CONN:
            CURSOR.execute(sql, (self.name, self.album))
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song

    @classmethod
    def new_from_db(cls, row):
        song = cls(row[1], row[2])
        song.id = row[0]
        return song

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM songs
        """
        with CONN:
            all_rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in all_rows]

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM songs
        """
        with CONN:
            all_rows = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all_rows]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM songs
            WHERE name = ?
            LIMIT 1
        """
        with CONN:
            song_row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(song_row)

# Example usage:
water = Song("Driving license", "Sour")
nf = Song("Mistake", "Hope")
barb = Song("Beef", "Barbie 2")

# Create the table if it doesn't exist
Song.create_table()

# Save songs to the database
water.save()
nf.save()
barb.save()

# Retrieve all songs from the database
all_songs = Song.get_
