from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

poke = pd.read_csv("Pokemon.csv")
def combination(i):
    return str(i['Type 1'])+ '$' +str(i['Generation'])+'$'+str(i['Legendary'])
poke['Atribute']= poke.apply(combination,axis=1)
poke['Name']= poke['Name'].apply(lambda i: i.lower())

cov = CountVectorizer(tokenizer=lambda poke: poke.split('$'))
pokeUlti = cov.fit_transform(poke['Atribute'])
skorPoke = cosine_similarity(pokeUlti)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('pokemon.html')

@app.route('/hasil', methods=['GET','POST'])
def Cari():
    body = request.form
    pokesuka = body['pokemon']
    pokesuka = pokesuka.lower()
    if pokesuka not in list(poke['Name']):
        return redirect('/NotFound')
    indexSuka = poke[poke["Name"] == pokesuka].index[0]
    favorit = poke.iloc[indexSuka][["Name",'Type 1','Generation','Legendary']]
    url = 'https://pokeapi.co/api/v2/pokemon/'+ pokesuka
    url = requests.get(url)
    picReko = url.json()["sprites"]["front_default"]
    pokeRekom = list(enumerate(skorPoke[indexSuka]))
    pokeSamaSortir = sorted(pokeRekom, key= lambda x:x[1], reverse= True)
    Rekom=[]
    for item in pokeSamaSortir[:7]:
        x={}
        if item[0] != indexSuka:
            nama = poke.iloc[item[0]]['Name'].capitalize()
            type = poke.iloc[item[0]]['Type 1']
            legend = poke.iloc[item[0]]['Legendary']
            gen = poke.iloc[item[0]]['Generation']
            url = 'https://pokeapi.co/api/v2/pokemon/'+ nama.lower()
            url = requests.get(url)
            pic = url.json()["sprites"]["front_default"] 
            x['Name']= nama
            x['Type']= type
            x['Legend']= legend
            x['Generation']= gen
            x["gambar"] = pic
            Rekom.append(x)
    return render_template('hasil.html',rekomendasi= Rekom, favorit= favorit, pic=picReko)


@app.route('/NotFound')
def notFound():
    return render_template('no.html')


if __name__=='__main__':
    app.run(debug=True)