#!/usr/bin/python

# Usage:
#
#  % ./extract-tweets.py csv-file output-file-fragment  n
#
# This script will process csv-file and produce three output files:
#  output-file-fragment-1.csv
#  output-file-fragment-2.csv
#  output-file-fragment-3.csv
# with n tweets each for manual classification.

import csv
import db_glue
import sys

tweet_data = csv.reader(open(sys.argv[1]), delimiter = ',', quotechar='"')

out_files = dict()
for i in range(1, 4):
    out_files[i] = csv.writer(open(sys.argv[2] + '-' + str(i) + '.csv', 'w'),
                              delimiter = ',',
                              quotechar='"')

index = 0
limit = int(sys.argv[3])
for row in tweet_data:
    out_files[1 + (index % 3)].writerow([row[11], 'Enter Category Here'])
    index = index + 1
    if index > (limit * 3):
        break
