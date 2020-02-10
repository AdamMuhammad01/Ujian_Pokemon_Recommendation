import pandas as pd
import numpy as np
import json
import requests
from flask import Flask, render_template, url_for, request, abort, redirect, send_from_directory, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rekomendasi',methods=['POST','GET'])
def rekomendasi():
    if request.method == 'POST':
        body = request.form
        favorit = body['name'].capitalize()

        if favorit not in list(df['Name']):
            return redirect('/notfound')
        index = df[df['Name']==favorit].index.values[0]
        # print(stat)
        rekomen = sorted(list(enumerate(cos_score[index])),key=lambda x:x[1],reverse=True) 
        poke1 = df.iloc[index][col]
        # print(poke1)
        poke2 = []
        for i in rekomen:
            poke_x = {}
            if i[0] == index:
                continue
            else:
                num = df.iloc[i[0]]['#']
                name = df.iloc[i[0]]['Name']
                tipe = df.iloc[i[0]]['Type 1']
                gen = df.iloc[i[0]]['Generation']
                legend = df.iloc[i[0]]['Legendary']
                poke_x['num'] = num
                poke_x['name'] = name
                poke_x['tipe'] = tipe
                poke_x['gen'] = gen
                poke_x['legend'] = legend
            poke2.append(poke_x)
            if len(poke2) == 6:
                break
        # print(poke2)
    return render_template('rekomen.html',rekomen = poke2, favoritku = poke1)


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == "__main__":
    df = pd.read_csv('Pokemon.csv')
    df['Legendary'] = df['Legendary'].replace({False:'Not Legend',True: 'Legend'})
    col = ['#','Name','Type 1','Generation','Legendary']
    df = df[col]
    df['compare'] = df.apply(lambda i: f"{i['Type 1']},{(i['Generation'])},{(i['Legendary'])}",axis = 1)

    model = CountVectorizer(tokenizer= lambda x:x.split(','))
    model_extract = model.fit_transform(df['compare'])

    cos_score = cosine_similarity(model_extract)

    app.run(debug=True)