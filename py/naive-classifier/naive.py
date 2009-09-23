#!/usr/bin/env python

from os import sys;
sys.path.append('/export/scratch/morten/software/nltk-2.0b5');

import nltk

# read in dictionaries
happyWords = [];
sadWords = [];

happyFile = open("../../dict/happy.txt", 'r');
for line in happyFile.readlines():
    word = line.strip();
    happyWords.append(word);
happyFile.close();

sadFile = open("../../dict/sad.txt", 'r');
for line in sadFile.readlines():
    word = line.strip();
    sadWords.append(word);
sadFile.close();


# read in prefixes
prefixes = [];

prefixFile = open("../../dict/prefixes.txt", 'r');
for line in prefixFile.readlines():
    word = line.strip();
    prefixes.append(word);
prefixFile.close();

# could perhaps also use set(list) to make sure there's no duplicates
# in our word list

featureSet = [];

# for each prefix
for prefix in prefixes:
    # add (prefix + word, class) to feature set
    prefixFeature = "contains-word(%s)" % prefix;
    for happyword in happyWords:
        wordFeature = "contains-word(%s)" % happyword;
        featureSet.append((dict([(prefixFeature, 1), (wordFeature, 1)]),'isHappy'));
    for sadword in sadWords:
        wordFeature = "contains-word(%s)" % sadword;
        featureSet.append((dict([(prefixFeature, 1), (wordFeature, 1)]),'isSad'));

# train the classifier
classifier = nltk.NaiveBayesClassifier.train(featureSet);

# test the classifier on our tweets
import csv;

# follower_count = tweet[1]
# friend_count = tweet[2]
# status_count = tweet[8] (num tweets)

tweet_data = csv.reader(open(sys.argv[1]), delimiter = ',', quotechar='"');
print "Tweets\tFollowers\tFriends\tHappy\tSad";
for tweet in tweet_data:

    numFollowers = tweet[1];
    numFriends = tweet[2];
    numTweets = tweet[8];

    probHappy = 0.0;
    probSad = 0.0;

    tweetContent = tweet[11];
    # tokenize tweet
    tweetTokens = nltk.word_tokenize(tweetContent);
    # create featureset
    # lowercase words
    tweetFeatures = ["contains-word(%s)" % word.lower() for word in tweetTokens];
    featureSet = {};
    for feature in tweetFeatures:
        featureSet[feature] = 1;
    probDist= classifier.prob_classify(featureSet);
    for sample in probDist.samples():
        prob = probDist.prob(sample);
        if(sample == "isHappy"):
            probHappy = prob;
            probSad = 1 - probHappy;
        elif(sample == "isSad"):
            probSad = prob;
            probHappy = 1 - probSad;

    print "%s\t%s\t%s\t%f\t%f" % (numTweets, numFollowers, numFriends, probHappy, probSad);
