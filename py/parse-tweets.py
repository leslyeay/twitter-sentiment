#!/usr/bin/python

# Usage:
#
#  % ./parse-tweets.py csv-file > sql-file
#
# Then, run sql-file in your database.

import csv
import db_glue
import sys

filename = sys.argv[1]
tweet_data = csv.reader(open(filename), delimiter = ',', quotechar='"')

db = db_glue.DB()

for row in tweet_data:
    sql = """
INSERT INTO tweet (
   is_favorited,
   follower_count,
   friend_count,
   in_reply_screen_name,
   in_reply_status_id,
   in_reply_user_id,
   screen_name,
   src,
   status_count,
   tweet_id,
   username,
   tweet
) VALUES (
   %s, %d, %d, %s, %d, %d, %s, %s, %d, %d, %s, %s
);
    """ % (row[0],
           int(row[1]),
           int(row[2]),
           db.quoted(row[3]),
           int(row[4]),
           int(row[5]),
           db.quoted(row[6]),
           db.quoted(row[7]),
           int(row[8]),
           int(row[9]),
           db.quoted(row[10]),
           db.quoted(row[11]))

    print(sql)
