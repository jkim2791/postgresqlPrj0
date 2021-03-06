# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("""
create table if not exists songplays(songplay_id BIGSERIAL PRIMARY KEY,
                                    start_time TIMESTAMP NOT NULL,
                                    user_id INTEGER NOT NULL,
                                    level VARCHAR,
                                    song_id VARCHAR ,
                                    artist_id VARCHAR ,
                                    session_id VARCHAR ,
                                    location VARCHAR ,
                                    user_agent VARCHAR)
                                    """)
                                    

user_table_create = ("""
create table if not exists users(user_id INTEGER PRIMARY KEY,
                                 first_name varchar,
                                 last_name varchar, 
                                 gender VARCHAR,
                                 level VARCHAR)
                                 """)


song_table_create = ("""
create table if not exists songs(song_id VARCHAR PRIMARY KEY,
                                title varchar, 
                                artist_id VARCHAR ,
                                year int, 
                                duration DECIMAL)
""")

artist_table_create = ("""
create table if not exists artists(artist_id VARCHAR PRIMARY KEY,
                                  name varchar, 
                                  location varchar, 
                                  latitude VARCHAR, 
                                  longitude VARCHAR)
""")

time_table_create = ("""
create table if not exists time(start_time TIMESTAMP PRIMARY KEY,
                                hour int, 
                                day int, 
                                week int, 
                                month int, 
                                year int, 
                                weekday int)
""")


# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users
(user_id, first_name, last_name, gender, level)
VALUES(%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE
SET level = 'paid'
""")

song_table_insert = ("""
INSERT INTO songs
(song_id, title, artist_id, year, duration)
VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_id, name, location, latitude, longitude)
VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time
(start_time, hour, day, week, month, year, weekday)
VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, artists.artist_id
FROM songs
JOIN artists
ON songs.artist_id = artists.artist_id
WHERE songs.title = %s 
AND artists.name = %s
AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]