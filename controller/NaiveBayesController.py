from sklearn.model_selection import train_test_split
from .helper.extension_checker import allowed_file
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import string
# from nltk.corpus import stopwords
from sklearn.externals import joblib
import json
import numpy as np
import pandas as pd


def NaiveBayesController(request, db):
    email = request.form['email']
    model_name = request.form['model_name']

    if request.form['process'] == 'train':
        dataset = request.files['data']
        if not allowed_file(dataset.filename):
            return 'file not allowed'
        message_name = request.form['message_column']
        label_name = request.form['label_column']
        test_size = float(request.form['test_size'])

        try:
            df = pd.read_csv(dataset)
        except Exception as e:
            return 'unable to read file '+e

        try:
            X_data = df[message_name]
            label = df[label_name]

        except Exception as e:
            return 'error occurred'+e
        X_train, X_test, y_train, y_test = train_test_split(X_data, label, test_size=test_size, random_state=101)
        print("loaded and splitted data")
        lr = Pipeline([
            ('bow', CountVectorizer()),  # strings to token integer counts
            ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
            ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
            ])

        lr.fit(X_train, y_train)
        try:
            db.addUserModel(email, 'naivebayes', model_name)
            joblib.dump(lr, 'trained_models/'+'naivebayes_model'+email+model_name+'.pkl')
        except Exception as e:
            return 'unable to save trained model '+e

        return 'Ok model trained'
    
    x = request.form['x']
    x = pd.Series(x)
    try:
        lr = joblib.load('trained_models/'+'naivebayes_model'+email+model_name+'.pkl')
        return " ".join(list(map(str, lr.predict(x))))
    except Exception as e:
        return 'unable to load trained model '+e
    
def text_process(mess):
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]