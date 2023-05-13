from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.filedialog import  askopenfilename
from tkinter import messagebox as mb
from tkinter import *
root = tk.Tk()
root.title('Profanity Scanner')
root.resizable(False, False)
root.geometry('330x150')
filename1 = None
file_contents = ''
emptyText = ''
textLabel = Label(text="Select text that file\nneeds to be scanned: ").place(x=100, y=10)

def answerFunction(text1, words):

    if text1 == 'Text is NEGATIVE!':
        badWords = ''
        for word in words:
            badWords += word + ','
        mb.showinfo("Information", "The text is negative\n Bad words are: %s" % (badWords))
    else:
        mb.showerror("Result", text1)

def mainFunction(SampleText):
    sa = SentimentIntensityAnalyzer()
    score = sa.polarity_scores(SampleText)

    print(score['compound'])

    tokens = SampleText.lower().split()

    clean_tokens = tokens[:]

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)

    freq = nltk.FreqDist(clean_tokens)

    freq.plot(20, cumulative=False)

    for key,val in freq.items():
        print(str(key) + ':' + str(val))

    print(clean_tokens)

    def get_part_of_speech_tags(token):
        tag_dict = {"J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV}

        tag = nltk.pos_tag([token])[0][1][0].upper()
        return tag_dict.get(tag, wordnet.NOUN)

    lemmatizer = WordNetLemmatizer()

    swearWordsList = (["fuck", "shit", "bitch", "bastard", "slut", "twat", "fucker", "faggot", "fucking"])
    swearWordsInText = ([])

    for token in tokens:
        lemmatisedtoken = lemmatizer.lemmatize(token, get_part_of_speech_tags(token))
        print(token, lemmatisedtoken)
        for word in swearWordsList:
            if word == token:
                print("Swear word detected!", token)
                swearWordsInText.append(token)

    vectorizer = TfidfVectorizer()
    tf_idf_matrix = vectorizer.fit_transform(tokens)
    print(vectorizer.get_feature_names_out())
    print(tf_idf_matrix.toarray())

    g = open("record.txt", "a")

    if score['compound'] > 0:
        print("text is positive")
        g.write("\nThe sampled text is POSITIVE!"+ " "+ str(score['compound']))
        textIs = 'Text is POSITIVE!'
    elif(score['compound'] == 0):
        g.write("\nThe sampled text is NEUTRAL!"+ " "+ str(score['compound']))
        print("The sampled text is NEUTRAL!")
        textIs = 'Text is NEUTRAL!'
    else:
        g.write("\n(The sampled text is NEGATIVE!"+ " "+ str(score['compound'])+")")
        print("The sampled text is NEGATIVE!")
        textIs = 'Text is NEGATIVE!'
        for words in swearWordsInText:
            g.write(" " + words+ " ")

    answerFunction(textIs, swearWordsInText)

def select_file():

    filename1 = askopenfilename()
    print('Selected: ', filename1)

    with open(filename1, 'r') as file:
        file_contents = file.read()

    print(file_contents)

    if file_contents == '':
        print("Please select file with contents!")
    else:
        mainFunction(file_contents)

open_button = ttk.Button(
    root,
    text='Select File',
    command=select_file
)

open_button.pack(expand=True)

root.mainloop()




