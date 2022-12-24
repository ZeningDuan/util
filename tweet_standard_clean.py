import csv
import gensim, logging
import re
import nltk
import pandas as pd
import numpy as np
import preprocessor as p
from gensim.utils import tokenize
from nltk.tokenize import word_tokenize
import spacy
nlp = spacy.load('/usr/local/lib/python3.7/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')
all_stopwords = nlp.Defaults.stop_words
#all_stopwords


def RemoveURLnEMOJI(string):
    p.set_options(p.OPT.EMOJI, p.OPT.URL)
    cleanstr = p.clean(string)
    return(cleanstr)


def RemoveShortWord(string): #remove words with one or two letters
    cleanstr = ' '.join( [w for w in string.split() if len(w)>2] )
    return cleanstr


def RemoveNonAscii(string):
    encoded_string = string.encode("ascii", "ignore")
    cleanstr = encoded_string.decode()
    return cleanstr


def RemovePunc(string, mode = 1):
    if mode == 1: #with @ and #
        punc = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~@#'
    if mode == 0:
        punc = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~'

    for ele in string:
        if ele in punc:
            string = string.replace(ele, " ")
    cleanstr = string

    return cleanstr


def RemoveNonalpha(string):
    cleanstr = re.sub("[^a-zA-Z]"," ", string)
    return cleanstr


def ParseHashtag(string):
    def rep(m):
        s=m.group(1)
        return ' '.join(re.split(r'(?=[A-Z])', s))

    cleanstr = re.sub(r'#(\w+)', rep, string)
    return cleanstr


def RemoveRT(string): #remove all "RT @" to "@"
    z = lambda x:re.compile('RT @').sub('@', x, count=2).strip()
    cleanstr = z(string)
    return(cleanstr)


def RemoveMention(string):
    cleanstr = re.sub("@[A-Za-z0-9_]+","", string)
    return cleanstr


def RemoveWhiteSpace(string):
    newstr = string.strip()
    cleanstr = re.sub(" +", " ",newstr)
    return cleanstr


def RemoveSeparator(string):
    cleanstr = string.replace('\n','')
    cleanstr = cleanstr.replace('\t','')

    return cleanstr


def lowercase(string):
    cleanstr = string.lower()
    return cleanstr


def gettoken(string) -> list:
    text_tokens = tokenize(string)
    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    clean_ls = list(tokens_without_sw)
    #clean_ls = list(tokenize(string))
    return clean_ls


#**
def give_emoji_free_text(text):#Remove Emoji
    return emoji.get_emoji_regexp().sub("", text)
#**

#Pack all the remove functions defined above into one
def Preprocess(string):
    newstr = RemoveURLnEMOJI(string)
    newstr = RemoveShortWord(newstr)
    newstr = RemoveNonAscii(newstr)
    newstr = RemoveRT(newstr)
    newstr = RemovePunc(newstr, mode = 1)
    newstr = RemoveNonalpha(newstr)
    newstr = ParseHashtag(newstr)
    newstr = RemoveMention(newstr)
    newstr = RemoveWhiteSpace(newstr)
    newstr = RemoveSeparator(newstr)
    newstr = lowercase(newstr)
    clean_ls = gettoken(newstr)
    return clean_ls
