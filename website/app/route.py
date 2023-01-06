#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 5 Jan. 2023
# ==============================================================================

import mysql.connector
import joblib
import string as str
import re

from flask import render_template, redirect, request
from nltk.corpus import stopwords

from app import app
from .db import get_db_config, db_connect


path = "config.json"
config = get_db_config(path)

myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()




# Loading the NLP Sentiment Analysis Model
nlp = joblib.load('../nlp_sent_analysis.joblib')
vect = nlp['vectorizer']
model = nlp['model']

def sentiment_analysis(comment:str) -> int:
    """
    Sentiment Analysis to say if a comment is positif or negatif (1, 0)
    Start with a preprocessing for the comment treatment and return the
    prediction
    @Params :
        comment         - required : str (a comment to analyze)
    """

    # Lower Casing
    comment = comment.lower()

    # URL
    comment = re.sub(r"https?://\S+|www\.\S+", "", comment)

    # HTML Tag
    html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    comment = re.sub(html, "", comment)

    # Punctuation
    comment = comment.replace(r'[]!"\'$€%&()*+,./:;=#@?[\\^_`{|}~-]+', " ")

    # Extra Whitespaces
    comment = comment.replace(' +', ' ')

    # Stopwords
    comment = comment.split()
    stop = set(stopwords.words('french'))
    comment = [word for word in comment if word not in stop]
    comment = ' '.join(comment)

    # Vectorization (TDIDF)
    comment = vect.transform([comment])

    # Prediction
    predict = model.predict(comment)[0]

    return predict




@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

@app.route('/demo', methods=['GET','POST'])
def demo():
    if request.method == 'POST':
        comment = request.form["comment"]
        predict = sentiment_analysis(comment)
        return render_template('demo.html', title='Demo', predict=predict)
    else:
        return render_template('demo.html', title='Demo')
    # return render_template('demo.html', title='Demo')

@app.route('/scrap')
def scrap():
    return render_template('scrap.html', title='Scraping')

@app.route('/explore')
def explore():
    return render_template('explore.html', title='Explore')