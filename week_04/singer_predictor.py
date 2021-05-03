#!/usr/bin/env python 3.8.3
# coding: utf-8
"""
Dummy lyrics predictor
"""

# 1. imports
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import operator
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, cross_validate
import os
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

# 2. constants
filepath1 = '/home/guo/download/Taylor-Swift/'
filepath2 = '/home/guo/download/Michael-Jackson/'

# 3. function definitions
# clean text
def clean_text(text):
    clean_text = text.replace('\n', ' ').strip()
    return clean_text

def song_as_string(filepath):
    files = os.listdir(filepath)
    corpus = []
    i = 0
    for fn in files:
            # get filename名称的信息  
            filename = filepath + os.sep + files[i]    
            # read file
            if fn.endswith('txt'):
                text = open(filename).read()
                text_cl = clean_text(text)
                corpus.append(text_cl)
            i += 1
    return corpus

# clean text
def clean_text(text):
    clean_text = text.replace('\n', ' ').strip()
    return clean_text

# change the list in the file as strings in line
def lines_as_str(lyrics_lines):
    s_list = []
    for line in open(lyrics_lines):
        if line != '\n':
            n=0
            line = clean_text(line)
            s_list.append(line)
            n+=1  
    return s_list 

def predict_artist(lyrics_input):
    """returns the probable name of the artist given some text"""
    string1 = song_as_string(filepath1)
    string2 = song_as_string(filepath2)
    l1=len(string1)
    l2=len(string2)
    corpus = string1 + string2  
    labels = ['Taylor-Swift'] * l1  + ['MJ'] * l2
    data = {'star': labels, 'lyrics': corpus}
    df = pd.DataFrame(data)
    X = df.iloc[:,0:]
    y = df['star']
    # train test split
    Xtrain, Xtest, ytrain, ytest = tts(X,y,train_size=0.98)
     
    customStopWords = ["'s", "'t", "'m", "'re", "'ll","'ve","...", "ä±", "''", '``',\
                  '--', "'d", 'el', 'la']
    stop = list(stopwords.words('english')+customStopWords)
    stop.extend('000 10 20 45 58 65 4am 90 200 2000'.split())
    cv = TfidfVectorizer(stop_words=set(stop),min_df=0.0001,max_df=0.99,
                         ngram_range=(1,2))
    cv.fit(Xtrain)
    X1 = cv.fit_transform(Xtrain['lyrics']) 
    X_df = pd.DataFrame(X1.todense(), columns=cv.get_feature_names(), index=Xtrain['star'])

    m_lr = LogisticRegression(class_weight='balanced', C=0.01,)
    m_lr.fit(X_df, ytrain)
    
    lyrics_input_t = cv.transform([lyrics_input])  
    probs = m_lr.predict_proba(lyrics_input_t)
    #df1 = pd.DataFrame(probs)
    # score0 = df1.iloc[0,0]
    #if score0 > 0.50:
        #return  print('Taylor Swift','possibility is',score0)
    # else:
    return m_lr.predict(lyrics_input_t)

# 4. main program
# prediction with user input
'''import argparse
parser = argparse.ArgumentParser(description='my first program')
parser.add_argument("message", help="displays the string you use here")
args = parser.parse_args()'''

user = input('Which lyrics you have in your mind: ')
print('I bet this belongs to the singer:', predict_artist(user))