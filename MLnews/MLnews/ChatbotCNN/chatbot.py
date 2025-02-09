import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
import time
import webbrowser
import urllib.request
import urllib.parse 
from bs4 import BeautifulSoup
import requests
#from googlesearch import *
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from ..pythonvit5.sum_txt import sum_txt

lemmatizer = WordNetLemmatizer()
model = load_model('MLnews\ChatbotCNN\chatbot_model')
intents = json.loads(open('MLnews\ChatbotCNN\intents_VN.json').read())
words = pickle.load(open('MLnews\ChatbotCNN\words.pkl','rb'))
classes = pickle.load(open('MLnews\ChatbotCNN\classes.pkl','rb'))

#Predict
def clean_up(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[ lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def create_bow(sentence,words):
    sentence_words=clean_up(sentence)
    bag=list(np.zeros(len(words)))
    
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence,model):
    p=create_bow(sentence,words)
    res=model.predict(np.array([p]))[0]
    threshold=0.8
    results=[[i,r] for i,r in enumerate(res) if r>threshold]
    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    
    for result in results:
        return_list.append({'intent':classes[result[0]],'prob':str(result[1])})
    return return_list

def googleSearch(query):
    my_results_list = []  
    for i in googlesearch.search(query):  
        my_results_list.append(i)  
    return my_results_list

def uri_validator(x):
    try:
        result = urllib.parse.urlparse(x)
        return result.scheme and result.netloc
    except:
        return False


def get_response(return_list,intents_json, user_text):
    print(return_list)
    if len(return_list)==0:
        if uri_validator(user_text):
            return user_text
        else:
            tag='noanswer'
    else:    
        tag=return_list[0]['intent']
    if tag=='datetime':        
        print(time.strftime("%A"))
        print (time.strftime("%d %B %Y"))
        print (time.strftime("%H:%M:%S"))

    if tag=='google':
        """
        query=input('Enter query...')
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
            webbrowser.open("https://google.com/search?q=%s" % query)
        

        
        url = "https://bing-web-search1.p.rapidapi.com/search"

        querystring = {"q":"news","mkt":"en-us","safeSearch":"Off","textFormat":"Raw","freshness":"Day","setLang":"en-us","responseFilter":"Videos","count":"10"}

        headers = {
            "X-BingApis-SDK": "true",
            "X-RapidAPI-Key": "b7c72454fdmsh2586f6fc473a93ap1eb635jsn3cf9b58f29b8",
            "X-RapidAPI-Host": "bing-web-search1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        i = 0
        lst_search = []
        for val in response.json()['value']:
            lst_search.append(str(i) + ". " + val['name'] + "\n" + "("+val['url']+")"+"\n")
            i = i + 1
        return lst_search
        """
        #return(googleSearch(user_text))



    if tag=='weather':
        api_key='987f44e8c16780be8c85e25a409ed07b'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = input("Enter city name : ")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url) 
        x=response.json()
        print('Present temp.: ',round(x['main']['temp']-273,2),'celcius ')
        print('Feels Like:: ',round(x['main']['feels_like']-273,2),'celcius ')
        print(x['weather'][0]['main'])
        
    if tag=='news':
        main_url = " http://newsapi.org/v2/top-headlines?country=in&apiKey=bc88c2e1ddd440d1be2cb0788d027ae2"
        open_news_page = requests.get(main_url).json()
        article = open_news_page["articles"]
        results = [] 
          
        for ar in article: 
            results.append([ar["title"],ar["url"]]) 
          
        for i in range(10): 
            print(i + 1, results[i][0])
            print(results[i][1],'\n')
            """   
    if tag=='cricket':
        c = Cricbuzz()
        matches = c.matches()
        for match in matches:
            print(match['srs'],' ',match['mnum'],' ',match['status'])
    
    if tag=='song':
        chart=billboard.ChartData('hot-100')
        print('The top 10 songs at the moment are:')
        for i in range(10):
            song=chart[i]
            print(song.title,'- ',song.artist)
            
    if tag=='timer':        
        mixer.init()
        x=input('Minutes to timer..')
        time.sleep(float(x)*60)
        mixer.music.load('Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        
    if tag=='covid19':
        
        covid19=COVID19Py.COVID19(data_source='jhu')
        country=input('Enter Location...')
        
        if country.lower()=='world':
            latest_world=covid19.getLatest()
            print('Confirmed:',latest_world['confirmed'],' Deaths:',latest_world['deaths'])
        
        else:
                
            latest=covid19.getLocations()
            
            latest_conf=[]
            latest_deaths=[]
            for i in range(len(latest)):
                
                if latest[i]['country'].lower()== country.lower():
                    latest_conf.append(latest[i]['latest']['confirmed'])
                    latest_deaths.append(latest[i]['latest']['deaths'])
            latest_conf=np.array(latest_conf)
            latest_deaths=np.array(latest_deaths)
            print('Confirmed: ',np.sum(latest_conf),'Deaths: ',np.sum(latest_deaths))
            """

    list_of_intents= intents_json['intents']    
    for i in list_of_intents:
        if tag==i['tag'] :
            result= random.choice(i['responses'])
    return result

def response(text):
    return_list=predict_class(text,model)
    response=get_response(return_list,intents, text)
    temp = sum_txt(text)
    return temp
