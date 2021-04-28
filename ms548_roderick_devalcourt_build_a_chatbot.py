# author: Roderick DeValcourt
# project: Assignment: Build A Chatbot

# main menu design

# Main Menu

# 1. Provide Context (google)
# 2. Provide Context (wikipedia)
# 3. Save Json Context
# 4. Train NLTK/NLP
# 5. Chat
# 6. Quit


import re
import string
from datetime import datetime

import googlesearch
import requests
import wikipedia
from bs4 import BeautifulSoup
from lxml import html
from textblob import TextBlob

from chatbotwindow import ChatBotWindow
from convert_text_to_json import ConvertTextToJson
from trainingchatbot import TrainChatBot


def get_input(title) -> int:
    try:
        result = int(input(title))
    except ValueError:
        result = 0
    return result


def get_new_blob(title) -> TextBlob:
    inputted_text = input(title)
    result = TextBlob(inputted_text)
    return result


class Information:
    def __init__(self):
        self.result = ''
        self.url = ''
        self.text_input = ''

    def set_result(self, r):
        self.result = r

    def set_url(self, u):
        self.url = u

    def set_text_input(self, ti):
        self.text_input = ti

    def __str__(self):
        message_text = '{},{},{}\n'.format(self.text_input, self.url, self.result)
        return message_text


class queryUrl:
    def __init__(self):
        self.fallback = 'Sorry, I cannot think of a reply for that.'
        self.list_information = []

    def chatbot_query_wikipedia(self, query):

        try:

            res = wikipedia.search(query, results=10)
            for r in res:

                try:

                    r2 = wikipedia.page(r)
                    # print(r2.url)
                    # print(r2.content)
                    # tree = html.fromstring(r2.content)

                    soup = BeautifulSoup(r2.content, features="lxml")

                    article_text = ''
                    article = soup.findAll('p')
                    for element in article:
                        article_text += '\n' + ''.join(element.findAll(text=True))

                    scrubbed = article_text.encode("ascii", "ignore")
                    article_text = scrubbed.decode()

                    article_text = re.sub(' +', ' ', article_text)

                    article_text = article_text.replace('/\\ /g', '\\\\')

                    article_text = article_text.replace('\r', ' ')
                    article_text = article_text.replace('\n', ' ')
                    article_text = article_text.replace('\t', '')
                    article_text = article_text.replace('"', '\\"')

                    article_text = article_text.strip()

                    first_sentence = article_text.split('.')
                    first_sentence = first_sentence[0].split('?')[0]

                    chars_without_whitespace = first_sentence.translate(
                        {ord(c): None for c in string.whitespace}
                    )

                    if len(chars_without_whitespace) > 0:
                        info = Information()
                        info.url = r2.url
                        info.set_result(first_sentence)
                        info.set_text_input(query)

                        self.list_information.append(info)
                except Exception:
                    continue

        except wikipedia.exceptions.DisambiguationError as e:
            for s in e.options:
                result = self.fallback
                print(s)

    def chatbot_query_google(self, query):

        try:
            search_result_list = googlesearch.search(query, num_results=10, lang='en')

            howmany = len(search_result_list)

            for index in range(howmany):

                try:

                    page = requests.get(search_result_list[index])

                    url = search_result_list[index]

                    # url = requests.Request.url

                    tree = html.fromstring(page.content)

                    soup = BeautifulSoup(page.content, features="lxml")

                    article_text = ''
                    article = soup.findAll('p')
                    for element in article:
                        article_text += '\n' + ''.join(element.findAll(text=True))

                    scrubbed = article_text.encode("ascii", "ignore")
                    article_text = scrubbed.decode()

                    article_text = re.sub(' +', ' ', article_text)

                    article_text = article_text.replace('/\\ /g', '\\\\')

                    article_text = article_text.replace('\r', ' ')
                    article_text = article_text.replace('\n', ' ')
                    article_text = article_text.replace('\t', '')
                    article_text = article_text.replace('"', '\\"')

                    article_text = article_text.strip()

                    first_sentence = article_text.split('.')
                    first_sentence = first_sentence[0].split('?')[0]

                    chars_without_whitespace = first_sentence.translate(
                        {ord(c): None for c in string.whitespace}
                    )

                    if len(chars_without_whitespace) > 0:
                        info = Information()
                        info.url = url
                        info.set_result(first_sentence)
                        info.set_text_input(query)
                        self.list_information.append(info)

                except:
                    continue

        except Exception as e:
            print(e)


class Menu:

    def __init__(self):
        self.options = dict()
        self.valid_selection = False
        self.selection = 0
        self.text_input = ''
        self.keep_going = True
        self.ok = False
        self.when = datetime.now()
        self.display_output_list = []
        self.file_name = self.when.strftime("roderick_devalcourt_ms548_build_a_chatbot_log_%m_%d_%Y.txt")
        self.url = ''

    def __del__(self):
        if not self.ok:
            self.append_to_file()

    def __str__(self):
        result = ''
        for key in self.options:
            if key == 0:
                result += '{}\n'.format(self.options[0])
            else:
                result += '{}. {}\n'.format(key, self.options[key])
        return result

    def print_log(self, text_info):
        dt_string = self.when.strftime("%m/%d/%Y %I:%M:%S %p")
        formatted_output = '{}\n{}\n-------------\n'.format(dt_string, text_info)
        print(formatted_output)
        self.save_print_out(formatted_output)

    def save_print_out(self, text_info):
        self.display_output_list.append(text_info)

    def append_to_file(self):
        try:
            where_at = 0
            how_many = len(self.display_output_list)
            if how_many > 0:
                output_file = open(self.file_name, 'a')
                while where_at < how_many:
                    output = self.display_output_list[where_at]
                    output_file.write(output)
                    where_at += 1
                output_file.close()
            if not self.ok:
                self.ok = True
        except IOError:
            print('Error writing to file {}'.format(self.file_name))

    def set_option(self, opt, title):
        if opt not in self.options:
            self.options[opt] = title
        else:
            if opt in self.options:
                print('{} {}\n'.format(self.options[opt], 'already exists in menu'))

    def set_selection(self, sel):
        self.selection = sel

    def get_selection(self):
        sel = self.selection
        return sel

    def process(self):
        print('Menu.process() -- override it!')


class Main(Menu):

    def __init__(self):
        Menu.__init__(self)

        self.set_option(0, 'Main Menu')
        self.set_option(1, 'Provide Context (google)')
        self.set_option(2, 'Provide Context (wikipedia)')
        self.set_option(3, 'Save Json Context')
        self.set_option(4, 'Train NLTK/NLP')
        self.set_option(5, 'Chat')
        self.set_option(6, 'Quit')
        self.output = 'c:\\pythonProject1\\data\\result.txt'
        self.output_json = 'c:\\pythonProject1\\data\\result.json'
        self.sentence_list = []
        self.article_words = []
        self.url = ''
        self.result = []

    def process(self):
        while self.keep_going:
            self.print_log(self)
            opt = get_input('Please Choose: ')

            inputted_information = 'Please Choose: {}'.format(opt)
            self.print_log(inputted_information)

            self.set_selection(opt)
            self.process_selection()

    def process_selection(self):

        sel = self.get_selection()

        if sel == 0:
            self.valid_selection = False
            self.print_log('input a valid selection!')
            self.keep_going = True

        if sel in self.options:
            self.valid_selection = True
        else:
            self.valid_selection = False
            self.print_log('input a valid selection!')
            self.keep_going = True

            # 1. Provide Context (google)
            # 2. Provide Context (wikipedia)
            # 3. Save Json Context
            # 4. Train NLTK/NLP
            # 5. Chat
            # 6. Quit

        if self.valid_selection:
            if sel == 1:
                # 1. Provide Context (google)

                obj = get_new_blob('question/input >>')
                self.text_input = obj.__str__()

                if len(self.text_input) > 0:
                    self.print_log(self.text_input)

                q = queryUrl()
                q.chatbot_query_google(self.text_input)

                of = open(self.output, "a", encoding='utf8')
                for i in q.list_information:
                    self.result.append(i)
                    of.write(i.__str__())

                of.close()

            if sel == 2:
                # 2. Provide Context (wikipedia)

                obj = get_new_blob('question/input >>')
                self.text_input = obj.__str__()

                if len(self.text_input) > 0:
                    self.print_log(self.text_input)

                q = queryUrl()

                q.chatbot_query_wikipedia(self.text_input)

                of = open(self.output, "a", encoding='utf8')
                for i in q.list_information:
                    self.result.append(i)
                    of.write(i.__str__())

                of.close()

            if sel == 3:
                # 3. Save Json Context

                try:
                    how_many = len(self.result)
                    count = 0
                    of = open(self.output_json, "a", encoding='utf8')
                    of.write('{\"intents\": [\n')
                    while count < how_many:

                        # for i in self.result:

                        i = self.result[count]

                        # jsonStr = json.dumps(i.__dict__)
                        # of.write(jsonStr)

                        cttj = ConvertTextToJson()

                        jsonString = cttj.go(i.text_input)

                        of.write('     {\"tag\": \"query\",\n')
                        of.write('     \"patterns\": ')
                        of.write(jsonString)
                        of.write(',\n')
                        of.write('     \"responses\": [\"')
                        of.write(i.result)
                        of.write('\"],\n')
                        of.write('     \"context\": [\"')
                        of.write(i.url)
                        of.write('\"]\n')
                        if count < how_many - 1:
                            of.write('     },\n')
                        else:
                            of.write('     }]\n')

                        count += 1

                    of.write('}\n')
                    of.close()

                # {"intents": [
                #    {"tag": "query",
                #     "patterns": ["sentences go here"],
                #     "responses": ["response goes here"],
                #     "context": [""]
                #     },
                #    {"tag": "query",
                #     "patterns": ["sentences go here"],
                #     "responses": ["response goes here"],
                #     "context": [""]
                #     }
                # }

                except Exception as e:
                    print(e)

            if sel == 4:
                # 4. Train NLTK/NLP

                # file_name = 'intents.json'
                # file_name = 'results.json'
                # self.output_json = 'c:\\pythonProject1\\data\\result.json'

                file_name = 'c:\\pythonProject1\\data\\result.json'

                tcb = TrainChatBot()
                tcb.go(file_name)

            if sel == 5:
                # 5. Chat

                cbw = ChatBotWindow()
                cbw.go()

            if sel == 6:
                # 6. Quit
                self.keep_going = False


def run():
    m = Main()
    m.process()


run()
