from tkinter import *
import tkinter as tk
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.pyplot as pPlot
from matplotlib.figure import Figure
import numpy as npy
from PIL import Image
from tkcalendar import Calendar
import matplotlib.pyplot as plt
import pandas as pd
# [1] https://towardsdatascience.com/synonyms-and-antonyms-in-python-a865a5e14ce8
# [2] https://spacytextblob.netlify.app/docs/example
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import spacy
from nltk.corpus import wordnet
from spacytextblob.spacytextblob import SpacyTextBlob
import en_core_web_sm
import re

from wordcloud import STOPWORDS, WordCloud

nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")


def word_cloud(text):
    words = ""

    for word in text:
        words = words + str(word).replace("'", "")

    wordcloud = WordCloud(height=400, background_color='white', stopwords=STOPWORDS).generate(words)

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.annotate("Please close this window before continuing with the program", xy=(0.5, 0.9), xytext=(0, 10),
                 xycoords=('axes fraction', 'figure fraction'),
                 textcoords='offset points',
                 size=14, ha='center', va='bottom')
    plt.show()


def get_polarity(text):  # returns a number, if negative, then mood is sad, if positive it's happy

    doc = nlp(text)

    return doc._.polarity


def get_triggers_for_trend_analysis(text):
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(text)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    return nouns


nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

window = Tk()


def main():
    main = MainView(window)
    main.pack(side="top", fill="both", expand=True)
    window.title("HackerTracker")
    window.geometry('1200x600')
    window.mainloop()


def nlp_func(text):  # sentence

    # nlp = en_core_web_sm.load()
    # nlp.add_pipe("spacytextblob")

    pos_synonyms = []
    neu_synonyms = []
    neg_synonyms = []

    NLP_Words = []

    # NLP analysis of single-line text
    doc = list(nlp.pipe([text]))
    emotional_words = dict()

    if len(text) != 0:

        for word in doc:  # i am happy and sad
            # captures the emotional words
            for assessment in word._.assessments:
                tmp = assessment[0]
                polarity = assessment[1]
                for emotional_word in tmp:
                    emotional_words[str(emotional_word)] = float(polarity)

        # [(word, polarity)]

        for x in emotional_words:
            if (emotional_words[x] > 0):
                pos_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in pos_synonyms:
                            pos_synonyms.append(lm.name())
            elif (emotional_words[x] < 0):
                neg_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in neg_synonyms:
                            neg_synonyms.append(lm.name())
            # returns the synonyms of the emotional word(s)
            elif (emotional_words[x] == 0):
                neu_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in neu_synonyms:
                            neu_synonyms.append(lm.name())

        NLP_Words.append(pos_synonyms)  # list of lists [pos words[], neg words[]
        NLP_Words.append(neg_synonyms)
        NLP_Words.append(neu_synonyms)

        if not len(pos_synonyms) and not len(neg_synonyms):
            msg = ["The natural language processor could not generate any words."]
            return msg
        else:

            return NLP_Words

    else:
        msg = ["No text was detected"]
        return msg


def nlp_msg(text):  # sentence

    # nlp = en_core_web_sm.load()
    # nlp.add_pipe("spacytextblob")

    pos_synonyms = []
    neu_synonyms = []
    neg_synonyms = []

    NLP_Words = []

    # NLP analysis of single-line text
    doc = list(nlp.pipe([text]))
    emotional_words = dict()

    if len(text) != 0:

        for word in doc:  # i am happy and sad
            # captures the emotional words
            for assessment in word._.assessments:
                tmp = assessment[0]
                polarity = assessment[1]
                for emotional_word in tmp:
                    emotional_words[str(emotional_word)] = float(polarity)

        # [(word, polarity)]

        for x in emotional_words:
            if (emotional_words[x] > 0):
                pos_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in pos_synonyms:
                            pos_synonyms.append(lm.name())
            elif (emotional_words[x] < 0):
                neg_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in neg_synonyms:
                            neg_synonyms.append(lm.name())
            # returns the synonyms of the emotional word(s)
            elif (emotional_words[x] == 0):
                neu_synonyms.append(str(x))
                for syn in wordnet.synsets(str(x)):
                    for lm in syn.lemmas():
                        # if lm.name()in pos_synonyms :
                        # adds the snonym(s) to the synonyms list
                        if lm.name() not in neu_synonyms:
                            neu_synonyms.append(lm.name())

        NLP_Words.append(pos_synonyms)  # list of lists [pos words[], neg words[]
        NLP_Words.append(neg_synonyms)
        NLP_Words.append(neu_synonyms)

        if not len(pos_synonyms) and not len(neg_synonyms):
            msg = ["The natural language processor could not generate any words."]
            return msg
        else:
            # word_cloud(NLP_Words)
            # abc = NLP_Words
            # print("global " + str(abc))
            msg = ["Please exit the Word Cloud to continue!"]
            return msg

    else:
        msg = ["No text was detected"]
        return msg


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# home page
class HomePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")
        lbl = Label(self, text="Welcome to HackerTracker!", font=("Comic Sans MS", 50, 'bold'), bg="black",
                    fg="SpringGreen2")
        lbl.place(relx=0.5, rely=0.5, anchor="c")
        clear_btn = Button(self, text="Clear all data", bg="black", fg="white", command=lambda x=None: self.clear())
        clear_btn.place(relx=0.5, rely=0.85, anchor="c")

    def reset_clear(self):
        lbl = Label(self, text="                          ", font=("Comic Sans MS", 15, 'bold'), bg="black",
                    fg="SpringGreen2")
        lbl.place(relx=0.5, rely=0.9, anchor="c")

    def clear(self):
        with open("saveData.txt", "w") as file:
            file.truncate()
            file.close()
        with open("trend_data.txt", "w") as file:
            file.truncate()
            file.close()
        lbl = Label(self, text="Data cleared", font=("Comic Sans MS", 10, 'bold'), bg="black",
                    fg="SpringGreen2")
        lbl.place(relx=0.5, rely=0.9, anchor="c")


# Second page asking for date
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")
        lbl = Label(self, text="Please select today's date:  ", font=("Comic Sans MS", 40, 'bold'), bg="black",
                    fg='SpringGreen2')
        lbl.place(relx=.5, rely=.05, anchor="c")

        # cal = Calendar(self, selectmode="day", year=2021, month=6, day=21, selectforeground='pink', foreground='yellow', highlightcolor='pink', normalforeground='orange', font=("Comic Sans MS", 20))
        cal = Calendar(self, background="black", disabledbackground="black", bordercolor="black",
                       headersbackground="black", normalbackground="black", foreground='white',
                       normalforeground='white', headersforeground='white', font=("Comic Sans MS", 20))
        cal.place(relx=.5, rely=.5, anchor="c")
        self.calendar = cal

        # create spins to add date
        # month = Label(self, text="Month")
        # month.grid(column=0, row=1, sticky="")
        # spin = Spinbox(self, from_=1, to=12, width=5, format="%02.0f")
        # spin.grid(column=0, row=2, sticky="")

        # day = Label(self, text="Day")
        # day.grid(column=1, row=1, sticky="")
        # spin2 = Spinbox(self, from_=1, to=30, width=5, format="%02.0f")
        # spin2.grid(column=1, row=2, sticky="")

        # year = Label(self, text="Year")
        # year.grid(column=2, row=1, sticky="")
        # spin3 = Spinbox(self, from_=0000, to=9999, width=5, format="%04.0f")
        # spin3.grid(column=2, row=2, sticky="")        # spin3.grid(column=2, row=2, sticky="")


# Third page asking to select options
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")  # copy these 3 lines to make a new class
        self.date = ""
        # make checkbutton for multiselect
        lbl = Label(self, text="Select desired categories", font=("Comic Sans MS", 40, 'bold'), bg="black",
                    fg='SpringGreen2')
        lbl.place(relx=.5, rely=.05, anchor="c")

        self.sleep_state = IntVar()
        sleep = Checkbutton(self, text="Sleep", variable=self.sleep_state, font=("Comic Sans MS", 20),
                            bg="SpringGreen2",
                            fg='black', highlightbackground="SpringGreen2")
        sleep.place(relx=.28, rely=.2, anchor="c")

        self.exercise_state = IntVar()
        exercise = Checkbutton(self, text="Exercise", variable=self.exercise_state, font=("Comic Sans MS", 20),
                               bg="SpringGreen2",
                               fg='black', highlightbackground="SpringGreen2")
        exercise.place(relx=.28, rely=.3, anchor="c")

        self.caffeine_state = IntVar()
        caffeine = Checkbutton(self, text="Caffeine", variable=self.caffeine_state, font=("Comic Sans MS", 20),
                               bg="SpringGreen2",
                               fg='black', highlightbackground="SpringGreen2")
        caffeine.place(relx=.28, rely=.4, anchor="c")

        self.mood_state = IntVar()
        mood = Checkbutton(self, text="Mood", variable=self.mood_state, font=("Comic Sans MS", 20), bg="SpringGreen2",
                           fg='black',
                           highlightbackground="SpringGreen2")
        mood.place(relx=.28, rely=.5, anchor="c")

        self.confidence_state = IntVar()
        confidence = Checkbutton(self, text="Confidence", variable=self.confidence_state, font=("Comic Sans MS", 20),
                                 bg="SpringGreen2", fg='black', highlightbackground="SpringGreen2")
        confidence.place(relx=.48, rely=.2, anchor="c")

        self.screenTime_state = IntVar()
        screenTime = Checkbutton(self, text="Screen Time", variable=self.screenTime_state, font=("Comic Sans MS", 20),
                                 bg="SpringGreen2", fg='black', highlightbackground="SpringGreen2")
        screenTime.place(relx=.48, rely=.3, anchor="c")

        self.socializing_state = IntVar()
        socializing = Checkbutton(self, text="Socializing", variable=self.socializing_state, font=("Comic Sans MS", 20),
                                  bg="SpringGreen2", fg='black', highlightbackground="SpringGreen2")
        socializing.place(relx=.48, rely=.4, anchor="c")

        self.productivity_state = IntVar()
        productivity = Checkbutton(self, text="Productivity", variable=self.productivity_state,
                                   font=("Comic Sans MS", 20),
                                   bg="SpringGreen2", fg='black', highlightbackground="SpringGreen2")
        productivity.place(relx=.48, rely=.5, anchor="c")

        self.hygiene_state = IntVar()
        hygiene = Checkbutton(self, text="Hygiene", variable=self.hygiene_state, font=("Comic Sans MS", 20),
                              bg="SpringGreen2",
                              fg='black', highlightbackground="SpringGreen2")
        hygiene.place(relx=.68, rely=.2, anchor="c")

        self.categories = []

    def newCategories(self):
        self.categories = [self.sleep_state.get(), self.exercise_state.get(), self.caffeine_state.get(),
                           self.mood_state.get(),
                           self.confidence_state.get(), self.screenTime_state.get(), self.socializing_state.get(),
                           self.productivity_state.get(),
                           self.hygiene_state.get()]

    # https://likegeeks.com/python-gui-examples-tkinter-tutorial/


# Fourth Page prompting journaling input
class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")
        self.date = ""
        self.categories = []

        # choice_lbl = Label(self, text="Select Best Option", font=("Comic Sans MS", 40, 'bold'), bg="black", fg='SpringGreen2')
        # choice_lbl.place(relx=.5, rely=.05, anchor="c")

        # sleep
        sleep_label = Label(self, text="How many hours did you sleep last night?", font=("Comic Sans MS", 20, 'bold'),
                            bg="black", fg='white')
        # sleep_label.grid(row=0, column=0)
        self.sleepMenuVar = StringVar()
        sleepMenu = OptionMenu(self, self.sleepMenuVar, "0-3 hours", "3-5 hours", "6-8 hours", "9-11 hours",
                               "11+ hours")
        # sleepMenu.grid(row=0, column=1)

        # exercise
        exercise_label = Label(self, text="How many hours did you exercise today?", font=("Comic Sans MS", 20, 'bold'),
                               bg="black", fg='white')
        # exercise_label.grid(row=1, column=0)
        self.exerciseMenuVar = StringVar()
        exerciseMenu = OptionMenu(self, self.exerciseMenuVar, "0-3 hours", "3-5 hours", "6-8 hours", "9-11 hours",
                                  "11+ hours")
        # exerciseMenu.grid(row=1, column=1)

        # caffeine
        caffeine_label = Label(self, text="How much caffeine did you have today?", font=("Comic Sans MS", 20, 'bold'),
                               bg="black", fg='white')
        # caffeine_label.grid(row=2, column=0)
        self.caffineMenuVar = StringVar()
        caffeineMenu = OptionMenu(self, self.caffineMenuVar, "0-100 mg", "101-200 mg", "201-300 mg", "301-400 mg",
                                  "400+ mg")
        # caffeineMenu.grid(row=2, column=1)

        # mood
        mood_label = Label(self, text="How would you describe your mood today?", font=("Comic Sans MS", 20, 'bold'),
                           bg="black", fg='white')
        # mood_label.grid(row=3, column=0)
        self.moodMenuVar = StringVar()
        moodMenu = OptionMenu(self, self.moodMenuVar, "Sad/Mad", "Tired", "Neutral", "Content", "Happy")
        # moodMenu.grid(row=3, column=1)

        # Confidence
        con_label = Label(self, text="How would you describe your confidence today, 5 being most confident?",
                          font=("Comic Sans MS", 20, 'bold'), bg="black", fg='white')
        # con_label.grid(row=4, column=0)
        self.conMenuVar = StringVar()
        conMenu = OptionMenu(self, self.conMenuVar, "1", "2", "3", "4", "5")
        # conMenu.grid(row=4, column=1)

        # screen time
        screen_label = Label(self, text="How many hours of screen time did you have today?",
                             font=("Comic Sans MS", 20, 'bold'), bg="black", fg='white')
        # screen_label.grid(row=5, column=0)
        self.screenMenuVar = StringVar()
        screenMenu = OptionMenu(self, self.screenMenuVar, "0-3", "3-6", "6-9", "9-11", "11+")
        # screenMenu.grid(row=5, column=1)

        # socializing
        social_label = Label(self, text="How many hours did you spend socializing today?",
                             font=("Comic Sans MS", 20, 'bold'), bg="black", fg='white')
        # social_label.grid(row=6, column=0)
        self.socialMenuVar = StringVar()
        socialMenu = OptionMenu(self, self.socialMenuVar, "0-3", "3-6", "6-9", "9-11", "11+")
        # socialMenu.grid(row=6, column=1)

        # productivity
        prod_label = Label(self, text="How would you describe your productivity today, 5 being most productive?",
                           font=("Comic Sans MS", 20, 'bold'), bg="black", fg='white')
        # prod_label.grid(row=7, column=0)
        self.prodMenuVar = StringVar()
        prodMenu = OptionMenu(self, self.prodMenuVar, "1", "2", "3", "4", "5")
        # prodMenu.grid(row=7, column=1)

        # hygiene
        hy_label = Label(self, text="How would you rate your hygeine today, 5 being best?",
                         font=("Comic Sans MS", 20, 'bold'), bg="black", fg='white')
        # hy_label.grid(row=8, column=0)
        self.hyMenuVar = StringVar()
        hyMenu = OptionMenu(self, self.hyMenuVar, "1", "2", "3", "4", "5")
        # hyMenu.grid(row=8, column=1)

        self.labelList = [sleep_label, exercise_label, caffeine_label, mood_label, con_label, screen_label,
                          social_label, prod_label, hy_label]
        self.menuList = [sleepMenu, exerciseMenu, caffeineMenu, moodMenu, conMenu, screenMenu, socialMenu, prodMenu,
                         hyMenu]
        self.surveyResults = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.outputs = []

    def updatedCategories(self):
        iterr = 0
        counter = 0
        for i in self.categories:
            title = Label(self, text="Please answer the following questions",
                          font=("Comic Sans MS", 30, 'bold'), bg="black", fg='SpringGreen2')
            title.grid(row=0, column=0)


            if i == 1:
                self.labelList[iterr].grid(row=counter + 1, column=0)
                self.menuList[iterr].grid(row=counter + 1, column=1)
                counter += 1
            iterr += 1
        if counter == 0:
            error_label = Label(self, text="Please go back and select at least one category!",
                                font=("Comic Sans MS", 30, 'bold'), bg="black", fg='red')
            error_label.grid(row=0, column=0)
            error_label2 = Label(self, text="Next button is disabled until a category is selected",
                                 font=("Comic Sans MS", 15, 'bold'), bg="black", fg='red')
            error_label2.grid(row=1, column=0)

    def destroyGrid(self):
        for label in self.grid_slaves():
            label.grid_forget()

    def transition(self):
        self.outputs = [self.sleepMenuVar.get(), self.exerciseMenuVar.get(), self.caffineMenuVar.get(),
                        self.moodMenuVar.get(), self.conMenuVar.get(),
                        self.screenMenuVar.get(), self.socialMenuVar.get(), self.prodMenuVar.get(),
                        self.hyMenuVar.get()]


# Page 5 with plots
class Page5(Page):

    def genGraph(self, x_axis, y_axis, fir, sec, thi, four, fif, num, cat):
        self.display_vals.clear()
        self.display_dates.clear()
        count = 0
        for val in self.everything[num]:
            if val != 0:
                self.display_dates.append(self.dates[count])
                self.display_vals.append(val)
            count += 1

        data = {x_axis: self.display_dates,
                y_axis: self.display_vals
                }
        df = DataFrame(data, columns=[x_axis, y_axis])

        figure = plt.Figure(figsize=(5, 5), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self)
        # line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        line.get_tk_widget().place(relx=0.3, rely=0.15)
        df = df[[x_axis, y_axis]].groupby(x_axis).sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels([fir, sec, thi, four, fif])
        ax.set_xticks(range(len(self.display_dates)))
        ax.set_xticklabels(self.display_dates)
        ax.set_title(cat)
        ax.set_ylabel(y_axis)
        figure.autofmt_xdate()

    def graph(self):
        if self.cats.get() == 'Sleep':
            if self.categories[0] == 1:
                black_screen = Label(self, text="",
                                    font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Hours', '0-3', '3-5', '6-8', '9-11', '11+', 0, 'Sleep')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red',width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')

        if self.cats.get() == 'Exercise':
            if self.categories[1] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Hours', '0-3', '3-5', '6-8', '9-11', '11+', 1, 'Exercise')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='brown', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Caffeine':
            if self.categories[2] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Milligrams', '0-3', '3-5', '6-8', '9-11', '11+', 2, 'Caffeine')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='grey', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Mood':
            if self.categories[3] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Emotion', 'Sad/Mad', 'Tired', 'Neutral', 'Content', 'Happy', 3, 'Mood')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='pink', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Confidence':
            if self.categories[4] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Rating', '1', '2', '3', '4', '5', 4, 'Confidence')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='purple', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Screen Time':
            if self.categories[5] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Hours', '0-3', '3-6', '6-9', '9-11', '11+', 5, 'Screen Time')
                self.genGraph('Date', 'Hours', '0-3', '3-6', '6-9', '9-11', '11+', 6, 'Screen Time')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='blue', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Socializing Time':
            if self.categories[6] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Hours', '0-3', '3-6', '6-9', '9-11', '11+', 6, 'Socializing Time')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='yellow', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Productivity':
            if self.categories[7] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Rating', '1', '2', '3', '4', '5', 7, 'Productivity')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')
        if self.cats.get() == 'Hygeine':
            if self.categories[8] == 1:
                black_screen = Label(self, text="",
                                     font=("Comic Sans MS", 18, 'bold'), bg="black", fg='red', width=70, height=19)
                black_screen.place(relx=.5, rely=.55, anchor='c')
                self.genGraph('Date', 'Rating', '1', '2', '3', '4', '5', 8, 'Hygeine')
            else:
                error_label = Label(self, text="Please select a category you recorded information for!", font=("Comic Sans MS", 18, 'bold'), bg="black", fg='orange', width=60, height=18)
                error_label.place(relx=.5, rely=.55, anchor='c')

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")
        self.date = ""
        self.categories = []
        self.outputs = []
        self.inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dates = []
        self.everything = [[], [], [], [], [], [], [], [], []]
        self.display_dates = []
        self.display_vals = []
        graph_lab = Label(self, text="Plots", font=("Comic Sans MS", 40, 'bold'), bg="black", fg='SpringGreen2')
        graph_lab.place(relx=.5, rely=.05, anchor="c")
        self.cats = StringVar()
        self.catsMenu = OptionMenu(self, self.cats, 'Sleep', 'Exercise', 'Caffeine', 'Mood', 'Confidence', 'Screen Time',
                                   'Socializing Time', 'Productivity', 'Hygeine', command=lambda x=None: self.graph())
        self.catsMenu.grid(row=0, column=0)

    def destroyGrid(self):
        for label in self.grid_slaves():
            label.grid_forget()

    # def graph(self):
    #     data = {'Date': self.dates,
    #              'Hours of Sleep': self.everything[0]
    #              }
    #     df = DataFrame(data, columns=['Date', 'Hours of Sleep'])
    #
    #     figure = plt.Figure(figsize=(5, 5), dpi=100)
    #     ax = figure.add_subplot(111)
    #     line = FigureCanvasTkAgg(figure, self)
    #     # line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    #     line.get_tk_widget().place(relx=0.3, rely=0.15)
    #     df = df[['Date', 'Hours of Sleep']].groupby('Date').sum()
    #     df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
    #     ax.set_yticks([1, 2, 3, 4, 5])
    #     ax.set_yticklabels(['0-3', '3-5', '6-8', '9-11', '11+'])
    #     ax.set_xticks(range(len(self.dates)))
    #     ax.set_xticklabels(self.dates)
    #     ax.set_title('Sleep')
    #     ax.set_ylabel('Hours')

    def assignIndicies(self):
        if self.outputs[0] == "0-3 hours":
            self.inputs[0] = 1
        elif self.outputs[0] == "3-5 hours":
            self.inputs[0] = 2
        elif self.outputs[0] == "6-8 hours":
            self.inputs[0] = 3
        elif self.outputs[0] == "9-11 hours":
            self.inputs[0] = 4
        elif self.outputs[0] == "11+ hours":
            self.inputs[0] = 5

        if self.outputs[1] == "0-3 hours":
            self.inputs[1] = 1
        elif self.outputs[1] == "3-5 hours":
            self.inputs[1] = 2
        elif self.outputs[1] == "6-8 hours":
            self.inputs[1] = 3
        elif self.outputs[1] == "9-11 hours":
            self.inputs[1] = 4
        elif self.outputs[1] == "11+ hours":
            self.inputs[1] = 5

        if self.outputs[2] == "0-100 mg":
            self.inputs[2] = 1
        elif self.outputs[2] == "101-200 mg":
            self.inputs[2] = 2
        elif self.outputs[2] == "201-300 mg":
            self.inputs[2] = 3
        elif self.outputs[2] == "301-400 mg":
            self.inputs[2] = 4
        elif self.outputs[2] == "400+ mg":
            self.inputs[2] = 5

        if self.outputs[3] == "Sad/Mad":
            self.inputs[3] = 1
        elif self.outputs[3] == "Tired":
            self.inputs[3] = 2
        elif self.outputs[3] == "Neutral":
            self.inputs[3] = 3
        elif self.outputs[3] == "Content":
            self.inputs[3] = 4
        elif self.outputs[3] == "Happy":
            self.inputs[3] = 5

        if self.outputs[4] == "1":
            self.inputs[4] = 1
        elif self.outputs[4] == "2":
            self.inputs[4] = 2
        elif self.outputs[4] == "3":
            self.inputs[4] = 3
        elif self.outputs[4] == "4":
            self.inputs[4] = 4
        elif self.outputs[4] == "5":
            self.inputs[4] = 5

        if self.outputs[5] == "0-3":
            self.inputs[5] = 1
        elif self.outputs[5] == "3-6":
            self.inputs[5] = 2
        elif self.outputs[5] == "6-9":
            self.inputs[5] = 3
        elif self.outputs[5] == "9-11":
            self.inputs[5] = 4
        elif self.outputs[5] == "11+":
            self.inputs[5] = 5

        if self.outputs[6] == "0-3":
            self.inputs[6] = 1
        elif self.outputs[6] == "3-6":
            self.inputs[6] = 2
        elif self.outputs[6] == "6-9":
            self.inputs[6] = 3
        elif self.outputs[6] == "9-11":
            self.inputs[6] = 4
        elif self.outputs[6] == "11+":
            self.inputs[6] = 5

        if self.outputs[7] == "1":
            self.inputs[7] = 1
        elif self.outputs[7] == "2":
            self.inputs[7] = 2
        elif self.outputs[7] == "3":
            self.inputs[7] = 3
        elif self.outputs[7] == "4":
            self.inputs[7] = 4
        elif self.outputs[7] == "5":
            self.inputs[7] = 5

        if self.outputs[8] == "1":
            self.inputs[8] = 1
        elif self.outputs[8] == "2":
            self.inputs[8] = 2
        elif self.outputs[8] == "3":
            self.inputs[8] = 3
        elif self.outputs[8] == "4":
            self.inputs[8] = 4
        elif self.outputs[8] == "5":
            self.inputs[8] = 5

    def savetoFile(self):
        i = 0
        first = -1
        second = -1
        for char in self.date:
            if char == "/":
                if first != -1:
                    second = i
                    break
                else:
                    first = i
            i += 1
        lines = ""
        with open("saveData.txt", "r") as file:
            lines = file.readlines()
            file.close()
        with open("saveData.txt", "w") as file:
            repeat = False
            for line in lines:
                j = 0
                temp = ""
                first_occurrence = -1
                second_occurrence = -1
                for char in line:
                    if char == " ":
                        break
                    elif char == "/":
                        if first_occurrence != -1:
                            second_occurrence = j
                        else:
                            first_occurrence = j
                        temp += char
                    else:
                        temp += char
                    j += 1
                if not repeat and (
                        self.date == temp or int(self.date[second + 1:]) < int(temp[second_occurrence + 1:]) or \
                        (int(self.date[second + 1:]) == int(temp[second_occurrence + 1:]) and
                         int(self.date[0:first]) < int(temp[0:first_occurrence])) or \
                        (int(self.date[second + 1:]) == int(temp[second_occurrence + 1:]) and
                         int(self.date[0:first]) == int(temp[0:first_occurrence]) and
                         int(self.date[first + 1:second]) < int(temp[first_occurrence + 1:second_occurrence]))):
                    repeat = True
                    file.write(str(self.date))
                    file.write(" ")
                    for i in self.inputs:
                        file.write(str(i))
                        file.write(" ")
                    file.write("\n")
                    if self.date != temp:
                        file.write(line)
                else:
                    file.write(line)
            if not repeat:
                file.write(str(self.date))
                file.write(" ")
                for i in self.inputs:
                    file.write(str(i))
                    file.write(" ")
                file.write("\n")
            file.close()

    def grabFromFile(self):
        self.dates.clear()
        for x in range(9):
            self.everything[x].clear()
        with open("saveData.txt") as file:
            i = 0
            while (True):
                line = file.readline()
                if not line:
                    break
                else:
                    temp = ""
                    j = 0
                    for char in line:
                        if char == " ":
                            self.dates.append(temp)
                            line = line[j + 1:]
                            break
                        else:
                            temp += char
                            j += 1
                    temporary = line.split(" ")
                    temporary.pop()
                    for x in range(9):
                        self.everything[x].append(int(temporary[x]))
                    # self.everything[i] = line.split(" ")
                    # self.everything[i].pop()
                    i += 1


# NLP prompting user for input

class Page6(Page):

    def __init__(self, *args, **kwargs):
        self.nlpList = [[]]
        texts = ""
        Page.__init__(self, *args, **kwargs, bg="black")
        graph_lab = Label(self, text="Write a sentence or two about your day: ", font=("Comic Sans MS", 40, 'bold'),
                          bg="black",
                          fg='SpringGreen2')
        graph_lab.grid(row=0, column=1, columnspan=3)
        E1 = Entry(self, textvariable=texts, bd=2, width=50)
        E1.grid(row=2, column=1)
        blueButton = Button(self, text="Submit", fg="blue", command=lambda: self.getNLPWords(str(E1.get())))
        blueButton.grid(row=4, column=1)
        spacer = Label(self, text="The natural language processor could not generate any words.", justify='center',
                       font=("Comic Sans MS", 20, 'bold'), bg="black", fg='black')
        spacer.grid(row=5, column=1)
        self.output = []
        self.msg = [[]]

    def getNLPWords(self, word):
        regex = re.compile('[^a-zA-Z]')
        # First parameter is the replacement, second parameter is your input strin
        word = regex.sub(' ', word)

        self.savetoFile(self.date, get_polarity(word), get_triggers_for_trend_analysis(word))

        for label in self.grid_slaves():
            if len(self.grid_slaves()) < 6:
                break
            else:
                label.grid_forget()

        self.msg = nlp_msg(word)

        # for nlp_list in self.msg:  # self.nlpList = [pos[], neg[]] #self.nlpList[0]
        graph_this = Label(self, text=self.msg[0], justify='center',
                           font=("Comic Sans MS", 20, 'bold'), bg="black", fg='SpringGreen2')
        graph_this.grid(row=6, column=1)

        if self.msg == ["Please exit the Word Cloud to continue!"]:
            word_cloud(nlp_func(word))

    def savetoFile(self, new_date, new_polarity, new_hover_words):
        comma = ","
        i = 0
        first = -1
        second = -1
        for char in self.date:
            if char == "/":
                if first != -1:
                    second = i
                    break
                else:
                    first = i
            i += 1
        lines = ""
        with open("trend_data.txt", "r") as file:
            lines = file.readlines()
            file.close()
        with open("trend_data.txt", "w") as file:
            repeat = False
            for line in lines:
                j = 0
                temp = ""
                first_occurrence = -1
                second_occurrence = -1
                for char in line:
                    if char == ":":
                        break
                    elif char == "/":
                        if first_occurrence != -1:
                            second_occurrence = j
                        else:
                            first_occurrence = j
                        temp += char
                    else:
                        temp += char
                    j += 1
                if not repeat and (
                        self.date == temp or int(self.date[second + 1:]) < int(temp[second_occurrence + 1:]) or \
                        (int(self.date[second + 1:]) == int(temp[second_occurrence + 1:]) and
                         int(self.date[0:first]) < int(temp[0:first_occurrence])) or \
                        (int(self.date[second + 1:]) == int(temp[second_occurrence + 1:]) and
                         int(self.date[0:first]) == int(temp[0:first_occurrence]) and
                         int(self.date[first + 1:second]) < int(temp[first_occurrence + 1:second_occurrence]))):
                    repeat = True
                    file.write(str(new_date) + ":" + str(new_polarity) + ":" + str(comma.join(new_hover_words)))
                    file.write('\n')
                    if self.date != temp:
                        file.write(line)
                else:
                    file.write(line)
            if not repeat:
                file.write(str(new_date) + ":" + str(new_polarity) + ":" + str(comma.join(new_hover_words)))
                file.write('\n')
            file.close()


class scatter_plot():
    dates = []
    polarity_arr = []
    hover_values = []


class Page7(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")

        self.fig = Figure(figsize=(8, 5))
        self.a = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.scatter_plot = scatter_plot()

        self.button = Button(self, text="Click here to Generate My Analysis", command=self.plot)
        self.button.pack()

        # self.canvas.get_tk_widget().pack()

    def read_inputs(self):

        self.grabFromFile()

        x_arr = scatter_plot.dates
        x_arr.pop()
        y_arr = scatter_plot.polarity_arr

        return x_arr, y_arr

    def plot(self):
        self.a.cla()
        x, v = self.read_inputs()

        self.a.scatter(x, v, color='red')

        n = self.scatter_plot.hover_values
        for i, txt in enumerate(n):
            new_txt = ",".join(txt)
            self.a.annotate(new_txt, (x[i], v[i]))

        self.a.set_title("Happiness Index", fontsize=11)
        self.a.set_yticks([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
        self.a.set_yticklabels([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
        self.a.set_ylabel("Trend", fontsize=10)
        self.a.set_xlabel("Dates", fontsize=10)

        # CreateToolTip(button, "happy, sad, coffee")
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def grabFromFile(self):
        self.scatter_plot.dates.clear()
        self.scatter_plot.hover_values.clear()
        self.scatter_plot.polarity_arr.clear()
        with open("trend_data.txt") as file:
            i = 0
            while (True):
                line = file.readline()
                plot_data = line.split(":")  # [date, float, list of words]
                num = 0
                for x in range(len(plot_data)):
                    if num == 0:
                        self.scatter_plot.dates.append(str(plot_data[x]))
                    if num == 1:
                        self.scatter_plot.polarity_arr.append(float(plot_data[x]))
                    if num == 2:
                        self.scatter_plot.hover_values.append(plot_data[x].split(","))
                    num += 1

                if not line:
                    break


class Page8(Page):

    def __init__(self, window, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg="black")
        self.window = window
        graph_lab = Label(self, text="Thank You For Using HackerTracker!", font=("Comic Sans MS", 40, 'bold'),
                          bg="black",
                          fg='SpringGreen2')
        graph_lab.place(relx=0.5, rely=0.5, anchor="c")
        next_btn = Button(self, text="Exit", bg="SpringGreen2", command=lambda: close())
        next_btn.place(relx=0.5, rely=0.6, anchor="c")

        # exits GUI
        def close():
            self.window.destroy()
            exit()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # objects for each of the screens
        home = HomePage(self)
        date = Page2(self)
        options = Page3(self)
        choices = Page4(self)
        plots = Page5(self)
        nlp = Page6(self)
        trend_analysis = Page7(self)
        exit_page = Page8(window, self)

        # global variables
        global screens
        screens = [home, date, options, choices, plots, nlp, trend_analysis, exit_page]
        global num
        num = 0

        # create menu
        menu = Menu(window)
        new_item = Menu(menu)
        new_item.add_command(label='Next', command=lambda: self.goNext(num))
        new_item.add_command(label='Back', command=lambda: self.goBack(num))
        new_item.add_command(label='Exit', command=lambda: self.close())
        menu.add_cascade(label='File', menu=new_item)
        window.config(menu=menu)

        # make frames
        button_frame = tk.Frame(self, bg="gray")
        container = tk.Frame(self, bg="black")
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        # create next button
        next_btn = Button(button_frame, text="Next", bg="blue", command=lambda: self.goNext(num))
        next_btn.pack(side="right")
        # create back button
        back_btn = Button(button_frame, text="Back", bg="blue", command=lambda: self.goBack(num))
        back_btn.pack(side="left")
        # place screens into a container
        home.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        date.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        options.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        choices.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        plots.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        nlp.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        trend_analysis.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        exit_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        screens[0].show()

    # moves to next screen
    def goNext(self, index):
        if index < len(screens) - 1:
            global num
            if num == 1:
                screens[num + 1].date = screens[num].calendar.get_date()
            elif num == 2:
                screens[num + 1].date = screens[num].date
                screens[num].newCategories()
                screens[num + 1].categories = screens[num].categories
                screens[num + 1].updatedCategories()
            elif num == 3:
                screens[num + 1].date = screens[num].date
                screens[num + 1].categories = screens[num].categories
                screens[num].transition()
                screens[num + 1].outputs = screens[num].outputs
                screens[num + 1].assignIndicies()
                screens[num + 1].savetoFile()
                screens[num + 1].grabFromFile()
                # screens[num + 1].graph()
            elif num >= 4:
                screens[num + 1].date = screens[num].date
                screens[num + 1].categories = screens[num].categories

            empty = True
            for x in screens[3].categories:
                if x != 0:
                    empty = False
                    break

            if num != 3 or not empty:
                num += 1
                screens[index + 1].show()

    # move to prev screen
    def goBack(self, index):
        if index > 0:
            global num
            if num == 1:
                screens[num - 1].reset_clear()
            if num == 3:
                screens[num].destroyGrid()
            num -= 1
            screens[index - 1].show()

    # exits GUI
    def close(self):
        window.destroy()
        exit()


if __name__ == "__main__":
    main()
