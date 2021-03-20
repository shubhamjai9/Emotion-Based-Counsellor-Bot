#!/usr/bin/env python

def generate_class_txt():
    with open('intents.txt', 'r') as intents, open('sentiment.txt', 'r') as sentiment, open('class.txt', 'w') as classes:
        for line in intents:
            sentence = line.split(',')[0]
            classes.write('%s,intent\n' % sentence)

        for line in sentiment:
            sentence = line.split(',')[0]
            classes.write('%s,non_intent\n' % sentence)

def sentiment_txt():
    with open('positive.txt', 'r') as positive, open('negative.txt', 'r') as negative, open('neutral.txt', 'r') as neutral, open('question.txt', 'r') as question, open('sentiment.txt', 'w') as sentiment, open('is_question.txt', 'w') as is_question:
        for line in positive:
            sentiment.write(line)
            is_question.write('%s,sentiment\n' % line.split(',')[0])
        for line in negative:
            sentiment.write(line)
            is_question.write('%s,sentiment\n' % line.split(',')[0])
        for line in neutral:
            sentiment.write('%s,neutral\n' % line[:-1])
            is_question.write('%s,sentiment\n' % line[:-1])
        for line in question:
            sentence = line.split(',')[0]
            is_question.write('%s,question\n' % sentence)

sentiment_txt()
generate_class_txt()
