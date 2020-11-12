
##### DATABASE CONNECTION 

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";



#######################################################

import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import string
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import WordPunctTokenizer
nltk.data.path
from flask import Flask, render_template, url_for, request, jsonify, Response
import numpy as np
import pickle
import json
import pandas as pd
import random

app = Flask(__name__)

## data read

data= pd.read_csv('modify_review.csv')


df = data[['ProductId','UserId','Score','Summary','Sentiment','year','month']]
import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
        
        
@app.route("/")
def home():
    month = request.args.get("month")
    year = request.args.get("year")
    m=int(month)
    y=int(year)
    print(int(y))
    
    print(type(2))
    recomended = []
    if month and year:
        # r=df.query('year == y & month == m')
        # print(r)
        k=df[(df.month == m) & (df.year == y)].index.values
        total_review=len(k)
        print(total_review)
        # print(k)
        total_postive_review=len(df[(df.month == m) & (df.year == y) &(df.Sentiment == 'positive')])
        total_negative_review=len(df[(df.month == m) & (df.year == y) &(df.Sentiment == 'negative')])
        print(total_postive_review)
        for i in k:
            recommend = {}
            # print(i)
            recommend['ProductId'] = df[df.index==i]['ProductId'].iloc[0]
            recommend['Score'] = df[df.index==i]['Score'].iloc[0]
            recommend['Summary'] = df[df.index==i]['Summary'].iloc[0]
            recommend['Sentiment'] = df[df.index==i]['Sentiment'].iloc[0]
            recommend['year'] = df[df.index==i]['year'].iloc[0]
            recommend['month'] = df[df.index==i]['month'].iloc[0]
            recomended.append(recommend)
        # print(recomended)
        response = {'results': {'status': 200,'message': 'Success','total_review':total_review ,'total_positive_review':total_postive_review,'total_negative_review': total_negative_review,'product_review':recomended}}
    else:
        response = {'results': {'status': 200, 'message': 'no date month'}}    
    
    return Response(json.dumps(response,cls=NpEncoder), status=200)    

if __name__ == '__main__':
    app.run()
    