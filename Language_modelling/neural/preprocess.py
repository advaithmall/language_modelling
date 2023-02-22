import pandas
import numpy as np
import re
import sys
import pprint
import random
import math

d = 0.75
contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he shall / he will",
    "he'll've": "he will have",
    "he's": "he has / he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / how is",
    "i'd": "I had / I would",
    "i'd've": "I would have",
    "i'll": "I shall ",
    "i'll've": " I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had / it would",
    "it'd've": "it would have",
    "it'll": "it shall / it will",
    "it'll've": "it shall have / it will have",
    "it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she shall / she will",
    "she'll've": "she shall have / she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / so is",
    "that'd": "that would / that had",
    "that'd've": "that would have",
    "that's": "that has / that is",
    "there'd": "there had / there would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they shall / they will",
    "they'll've": "they shall have / they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what has / what is",
    "what've": "what have",
    "when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / where is",
    "where've": "where have",
    "who'll": "who shall / who will",
    "who'll've": "who shall have / who will have",
    "who's": "who has / who is",
    "who've": "who have",
    "why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you shall / you will",
    "you'll've": "you shall have / you will have",
    "you're": "you are",
    "you've": "you have"
}


address_forms = {" mr ",  " mr. ",  " mrs. ",
                 " mrs  "   "  dr  ",  "  dr.  ",  " mr ",  " mrs ",  " dr "}
person_pronouns = {" i ",  " you ",  " he ",
                   " she ",  " it ",  " we ",  " they "}
reflex_pronouns = {" myself ",  " yourself ",
                   " himself ",  " herself ",  " itself ",  " ourselves ",  " yourselves ",  " themselves "}
possesive_pronouns = {" mine ",  " yours ",  " his ",
                      " hers ",  " its ",  " ours ",  " theirs "}
demonstrative_pronouns = {" this ", " that ", " these ", " those "}
inter_pronouns = {" who ", " whom ", " whose ", " what ", " which "}
indefinite_pronouns = {" all ", " another ", " any ", " anybody ", " anyone ", " anything ", " both ", " each ", " either ", " everybody ", " everyone ", " everything ",
                       " few ", " many ", " neither ", " nobody ", " none ", " no one ", " nothing ", " one ", " other ", " several ", " some ", " somebody ", " someone ", " something "}
articles = {" a ", " an ", " the "}
third_pronouns = {" her ", " him ", " them "}


def tokenize(corpus_string):

    space_pattern = '\s+'
    url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                 '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    mention_regex = '@[\w\-]+'
    hashtag_regex = '#[\w\-]+'

    corpus_string = re.sub(space_pattern, ' ', corpus_string)
    corpus_string = re.sub(url_regex, 'URLHERE', corpus_string)
    corpus_string = re.sub(mention_regex, 'MENTIONHERE', corpus_string)
    corpus_string = re.sub(hashtag_regex, 'HASHHERE', corpus_string)

    corpus_string = corpus_string.replace("_", "")
    for word in contractions.keys():
        corpus_string = corpus_string.replace(word, contractions[word.lower()])
    corpus_string = re.sub(r'[^\w\s!?.]', ' ', corpus_string)

    for item in address_forms:
        corpus_string = corpus_string.replace(item, " addressform ")
    for item in person_pronouns:
        corpus_string = corpus_string.replace(item, " personpronoun ")
    for item in reflex_pronouns:
        corpus_string = corpus_string.replace(item, " reflexpronoun ")
    for item in possesive_pronouns:
        corpus_string = corpus_string.replace(item, " possespronoun ")
    for item in demonstrative_pronouns:
        corpus_string = corpus_string.replace(item, " demonpronoun ")
    for item in inter_pronouns:
        corpus_string = corpus_string.replace(item, " interpronoun ")
    for item in indefinite_pronouns:
        corpus_string = corpus_string.replace(item, " indefpronoun ")
    for item in articles:
        corpus_string = corpus_string.replace(item, " articlehere ")
    for item in third_pronouns:
        corpus_string = corpus_string.replace(item, " thirdpronoun ")

    #print(corpus_string)
    return re.split(r'[.!?]', corpus_string)
