#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 5 Jan. 2023
# ==============================================================================
# Code to test the model in the terminal
# ==============================================================================

import joblib
import string as str
import re

from nltk.corpus import stopwords


nlp = joblib.load('nlp_sent_analysis.joblib')
vect = nlp['vectorizer']
model = nlp['model']


def preprocessing(comment:str):
    """
    Preprocessing for the comment treatment
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

    return comment




try:
    comment = input("Entrer un commentaire : ")

    comment = preprocessing(comment)

    pred = model.predict(comment)

    if pred == 1:
        print("Votre commentaire est un commentaire positif !")
    else:
        print("Votre commentaire est un commentaire négatif !")

except Exception as e:
    print(e)