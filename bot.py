#!/usr/bin/env python
from __future__ import unicode_literals
import spacy
import random
import numpy as np
from sklearn.externals import joblib
import warnings
from stopwords import ENGLISH_STOP_WORDS

warnings.filterwarnings("ignore", category=DeprecationWarning)
nlp = spacy.load('en')
intent_analyzer = joblib.load('./intent.pkl')
question_analyzer = joblib.load('./question.pkl')
sentiment_analyzer = joblib.load('./sentiment.pkl')
class_analyzer = joblib.load('./class.pkl')
is_question_analyzer = joblib.load('./is_question.pkl')
user_name = None
greeting_responses = ['How may I help you?', 'What can I do for you?', 'How can I be of service to you?', 'My name is Counsellor bot, How can I help you?']
greetings = ['Hi!', 'Hey there!', 'Hello', 'Aloha!', 'Hey!']
user_name = None

def process_sentence(sentence):
    processed_words = []
    for word in sentence.split():
        if word.lower() == "i'm":
            processed_words.append("i")
            processed_words.append("am")
        elif word.lower() == "i'll":
            processed_words.append("i")
            processed_words.append("will")
        elif word[-1] == ',' or \
            word[-1] == '?' or \
            word[-1] == '.' or \
            word[-1] == '!': 
            word = word[:-1]
            processed_words.append(word)
        else:
            processed_words.append(word)
    return ' '.join(processed_words)

def extract_name(sentence):
    doc = nlp((sentence))
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent
    return None

def spacy_get_vec(sentence, filter_stopwords=False):
    vec = np.zeros(384)
    doc = nlp((sentence))
    for word in doc:
        if filter_stopwords:
            if word.lower_ in ENGLISH_STOP_WORDS:
                continue
        vec += word.vector
    return vec

def get_sentiment_vec(sentence):
    vec = np.zeros(768)
    doc = nlp((sentence))
    for i,word in enumerate(doc):
        if i < len(doc) -1:
            tempvec = np.append(word.vector, doc[i + 1].vector)
            vec += tempvec
        else:
            tempvec = np.append(word.vector, np.zeros(384))
            vec += tempvec
    return vec

def weather(sentence):
        return("I'm sorry to say but I do not know anything about whether",True,None)

def greet(sentence):
    ind = random.randint(0, len(greeting_responses) -1)
    return (greeting_responses[ind], True, None)


def bye(sentence):
    return ('Have a nice day!', False, None)

def where(sentence):
    return ('have a nice trip!', True, None)

def users_name(sentence):
    global user_name
    name = extract_name(sentence)
    if user_name is None and name is None:
        return ('You didn\'t tell me your name', True, users_name)
    if name is None and user_name is not None:
        return ('Hi %s :-)' % user_name, True, None)
    user_name = name
    return ('Hello %s :-D' % name, True, None)

def sorry(sentence):
    responses = ['Too bad :(', 'I am very sorry to hear that.', 'I feel sorry to know that :-(', 'I am sorry','I know how you    feel right now']
    return (responses[random.randint(0, len(responses) -1)], True, None)

def name(sentence):
    return ('My name is Consellor Bot', True, None)

def marriage(sentence):
    responses = ['Romance is not for me', 'I don\'t have any girlfriend', 'I am too young for that']
    return (responses[random.randint(0, len(responses) -1)], True, None)

def congrats(sentence):
    responses = ['Being positive is always good.', 'Happy to hear that :-)', 'Wow! :-D','You\'re are positive person. Great!']
    return (responses[random.randint(0, len(responses) -1)], True, None)

def bot(sentence):
    return 'I am a bot :P', True, None

def bad(sentence):
    return 'That\'s a bad word', True, None

def neutral(sentence):
    responses = ['Oh, ok!', 'Hmm', 'Ok', 'Alright', 'Ah', 'Oh']
    return (responses[random.randint(0, len(responses) -1)], True, None)

def bot_location(sentence):
    responses = ['I live in the cloud', 'I live on the server', 'As we speak I am replicating myself over the internet']
    return (responses[random.randint(0, len(responses) -1)], True, None)

def greet_response(sentence):
    responses = ['I am good, thanks!', 'Pretty good, thanks for asking %s' %
            (user_name if user_name is not None else '') , 'I am Ok', 'Everything is fine']
    return (responses[random.randint(0, len(responses) -1)], True, None)

intent_actions = {'greeting': greet, 'goodbye': bye, 'bad': bad, 'weather':weather, 'travel':where}
sentiment_actions = {'neg': sorry, 'pos': congrats, 'neu': neutral}
question_actions = {'users_name': users_name, 'name': name, 'marriage': marriage,
        'bot': bot, 'location': bot_location, 'greet_response': greet_response }

is_user_input_expected = True
original_intent = None
print(greetings[random.randint(0, len(greetings) - 1)] )
action = None
while is_user_input_expected:
    sew = raw_input()
    s = unicode(sew, "utf-8")
    #print(type(s))
    s = s.strip()
    alpha=0
    for letter in s:
        if(letter.isalpha()):
            alpha+=1
        if(alpha==0):
            print(eval(s))
            continue
    if s == '':
        continue
    vec = spacy_get_vec(s)
    is_intent = class_analyzer.predict(spacy_get_vec(s, True))[0] == 'intent'
    if not is_intent:
        is_question = is_question_analyzer.predict(vec)[0] == 'question'
        if is_question:
            question = question_analyzer.predict(vec)[0]
            #print('outside notNone')
            action = question_actions[question]
        else:
            sentiment = sentiment_analyzer.predict(get_sentiment_vec(s))[0]
            action = sentiment_actions[sentiment]
        bot_response,is_user_input_expected,action = action(s)
        #print('Question ND senti notNone')
        print(bot_response)
        continue
    else:    
        intent = intent_analyzer.predict(vec)[0]
        action = intent_actions[intent]
        bot_response, is_user_input_expected,action = action(s)
        #print('outside notNone')
        action = None
        print(bot_response)
