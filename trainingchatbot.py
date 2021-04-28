# https://data-flair.training/blogs/python-chatbot-project/

# author: Roderick DeValcourt
# project: Assignment: Build A Chatbot
# this handles training the chatbot nltk/nlp


import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import random


class TrainChatBot:
    def __init__(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '!']
        self.patterns = []

    def go(self, file_name):
        data_file = open(file_name, encoding='utf8').read()
        intents = json.loads(data_file)

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                # add self.documents in the corpus
                self.documents.append((w, intent['tag']))
                # add to our self.classes list
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
                if intent['patterns'] not in self.patterns:
                    self.patterns.append(intent['patterns'])

        # lemmatize, lower each word and remove duplicates
        self.words = [lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        # sort self.classes
        self.classes = sorted(list(set(self.classes)))
        # self.documents = combination between patterns and intents
        print(len(self.documents), "documents")
        # self.classes = intents
        print(len(self.classes), "classes", self.classes)
        # self.words = all self.words, vocabulary
        print(len(self.words), "unique lemmatized words", self.words)
        pickle.dump(self.words, open('words.pkl', 'wb'))
        pickle.dump(self.classes, open('classes.pkl', 'wb'))
        pickle.dump(self.patterns, open('patterns.pkl', 'wb'))

        # create our training data
        training = []
        # create an empty array for our output
        output_empty = [0] * len(self.classes)
        # training set, bag of self.words for each sentence
        for doc in self.documents:
            # initialize our bag of self.words
            bag = []
            # list of tokenized self.words for the pattern
            pattern_words = doc[0]
            # lemmatize each word - create base word, in attempt to represent related self.words
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            # create our bag of self.words array with 1, if word match found in current pattern
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)
            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        print("Training data created")

        # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        # fitting and saving the model
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save('c:\\pythonProject1\\data\\chatbot_trained_model.h5', hist)
        print("model created")
