# https://data-flair.training/blogs/python-chatbot-project/

# author: Roderick DeValcourt
# project: Assignment: Build A Chatbot
# this handles the chat window

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from tkinter import *


class ChatBotWindow:
    def __init__(self):
        self.model = load_model('c:\\pythonProject1\\data\\chatbot_trained_model.h5')
        self.intents = json.loads(open('c:\\pythonProject1\\data\\result.json').read())
        self.words = pickle.load(open('c:\\pythonProject1\\words.pkl', 'rb'))
        self.classes = pickle.load(open('c:\\pythonProject1\\classes.pkl', 'rb'))
        self.patterns = pickle.load(open('c:\\pythonProject1\\patterns.pkl', 'rb'))
        self.EntryBox = []
        self.ChatLog = []
        self.base = []
        self.scrollbar = []
        self.SendButton = []
        self.EntryBox = []
        self.ints = ''

    def clean_up_sentence(self, sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def predict_class(self, sentence):
        try:
            # filter out predictions below a threshold
            p = self.bow(sentence, self.words, show_details=False)
            res = self.model.predict(np.array([p]))[0]
            ERROR_THRESHOLD = 0.25
            results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
            # sort by strength of probability
            results.sort(key=lambda x: x[1], reverse=True)
            return_list = []
            for r in results:
                return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        except ValueError:
            return_list = []
        except Exception as e:
            return_list = []
        return return_list

    def getResponse(self, text):
        how_many = len(self.ints)
        count = len(self.intents)
        result = []
        if how_many > 0:
            if count > 0:
                tag = self.ints[0]['intent']
                list_of_intents = self.intents['intents']
                for i in list_of_intents:
                    if i['tag'] == tag:
                        for p in i['patterns']:
                            # print ('p: {}'.format(p))
                            if p in text:
                                for r in i['responses']:
                                    result.append(r)

        # print('result: {}\n'.format(result))
        messageText = ''
        lr = len(result)
        if lr > 0:
            messageText = random.choice(result)
        return messageText

    def chatbot_response(self, text):
        self.ints = self.predict_class(text)

        how_many = len(self.ints)
        res = ''

        if how_many > 0:
            res = self.getResponse(text)

        return res

    # Creating GUI with tkinter
    def send(self):
        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", END)
        if msg != '':
            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert(END, "You: " + msg + '\n\n')
            self.ChatLog.config(foreground="#442265", font=("Verdana", 12))
            res = self.chatbot_response(msg)
            self.ChatLog.insert(END, "Bot: " + res + '\n\n')
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)

    def go(self):
        self.base = Tk()
        self.base.title("Hello")
        self.base.geometry("400x500")
        self.base.resizable(width=FALSE, height=FALSE)
        # Create Chat window
        self.ChatLog = Text(self.base, bd=0, bg="white", height="8", width="50", font="Arial", )
        self.ChatLog.config(state=DISABLED)
        # Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self.base, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set
        # Create Button to send message
        self.SendButton = Button(self.base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                                 bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                                 command=self.send)
        # Create the box to enter message
        self.EntryBox = Text(self.base, bd=0, bg="white", width="29", height="5", font="Arial")
        # self.EntryBox.bind("<Return>", send)
        # Place all components on the screen
        self.scrollbar.place(x=376, y=6, height=386)
        self.ChatLog.place(x=6, y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)
        self.base.mainloop()
