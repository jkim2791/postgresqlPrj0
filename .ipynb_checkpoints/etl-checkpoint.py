import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def get_files(filepath):
    '''
    this function reads json files to insert data into tables
    '''
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files


def process_song_file(cur, filepath):
    '''
    - Read json formated song file as dataframe and divide into two tables which are song_data and artist_data
    - Insert data into tables
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)
    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0]
    song_data = list(song_data)
    cur.execute(song_table_insert, song_data)
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0]
    artist_data = list(artist_data)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    - Read json formated log file as dataframe and divide into two tables which are ts_df and time_df
    - Insert data into tables
    '''
    # open log file
    log_df = pd.read_json(filepath, lines=True)
    # filter by NextSong action
    log_df = log_df[log_df['page']=="NextSong"]
    ts_df = log_df[['ts']]
    ts_df = log_df[log_df['page']=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(ts_df['ts'], unit='ms')

    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.dayofweek]
    column_labels = ['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = log_df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    log_df = log_df.drop_duplicates().dropna()
    for index, row in log_df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songId, artistId = results
        else:
            songId, artistId = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songId, artistId, row.sessionId, row.location, row.userAgent)


        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    test for inserting data from filepath
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''
    - connect to the database
    - process all data
    - close the database connection
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
