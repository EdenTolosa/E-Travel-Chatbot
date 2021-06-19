#import necessary libraries
import pyttsx3, datetime, os
import enchant
from enchant.checker import SpellChecker
import engineio as engineio
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages





def say(s):
        engineio = pyttsx3.init()
        rate = engineio.getProperty('rate')
        engineio.setProperty('rate', 200)
        voices= engineio.getProperty('voices')
        #for voice in voices:                                                                                    
        engineio.setProperty('voice', voices[1].id)
        #print voice.id                                                                                          
        engineio.say(s)
        a = engineio.runAndWait() #blocks     


# uncomment the following only the first time
nltk.download('punkt') 
nltk.download('wordnet') 

with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)#
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "hey there", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! thanks for using the bot"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            say (random.choice(GREETING_RESPONSES))
            return random.choice(GREETING_RESPONSES)
            



# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"


        chkr = SpellChecker("en_UK","en_US")
        spacedfile = user_response
        chkr.set_text(spacedfile)
        for err in chkr:
            sug = err.suggest()[0]
            err.replace(" %s" % ( sug))  
        Spellchecked = chkr.get_text()
        print ("Do you mean, suggested word :"+Spellchecked) # suggest words which has spelling error and return the right spelling
        say ("I am sorry! I don't understand you")
        say("Do you mean" + Spellchecked + " please type again as suggested")

        
        return robo_response


    else:
        robo_response = robo_response+sent_tokens[idx]
        chala = robo_response.split()[-1]
        # print (chala)
        say (robo_response)
        say ("to know more about this"+user_response+ " please go to our website or leave us comment" )

        return robo_response





flag=True
print ( "|| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("|| Welcome: I am your travelbot. I will answer your queries about etravel. If you want to exit, type Bye!")
print ( "|| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
say ("Welcome: I am your travelbot. I will answer your queries about etravel. If you want to exit, type Bye!")
while(flag==True):
    user_response = input("|| Please put your query about etravel here: ")
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("|| You are welcome..")
            print ( "|| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            say ("|| You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("|| Welcome : "+greeting(user_response))
                print ( "|| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                print("|| Here is your result : ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
                print ( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ||")
    else:
        flag=False
        print("|| Bye! take care and stay safe..")    
        say("Bye! take care and stay safe..")    
        
        

