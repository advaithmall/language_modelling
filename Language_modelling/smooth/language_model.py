import pandas
import numpy as np
import re
import sys
import pprint
import random
import math
import sys
file_n = sys.argv[2]
smooth_type = sys.argv[1]
#print(file_n, "->file" ,smooth_type,"-> smooth")
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

    return corpus_string


def get_lambda(hist_tuple):
    hist_len = len(hist_tuple)
    curr_gram = n_grams[hist_len-1]
    denom = curr_gram.get(hist_tuple, unk_cnt[hist_len])
    num = 1
    less_gram = n_grams[hist_len]
    for item in less_gram.keys():
        ch_tup = tuple(item.split()[:-1])
        # print(ch_tup)
        if hist_tuple == ch_tup:
            num += 1
    return ((num*d)/denom)


def get_count(sent, flag, glob_n):
    loc_len = len(sent)
    temp_str = " ".join(map(str, sent))
    gram = n_grams[loc_len-1]
    if flag == 1:
        if loc_len == glob_n:
            return gram.get(temp_str, 0)
        elif loc_len < glob_n:
            cont_count = 0
            cont_gram = n_grams[loc_len-1]
            for item in cont_gram.keys():
                cont_list = item.split()[-1]
                if cont_list == sent[-1]:
                    cont_count += 1
            return cont_count
    if flag == 0:
        return gram.get(temp_str, 0)


def kn_fincount(sing_word):
    sin_count = 0
    for item in bi_grams.keys():
        item_tup = tuple(item.split())
        if str(sing_word[0]) == str(item_tup[1]):
            sin_count += 1
    return sin_count


def get_witten(loc_tup):
    length = len(loc_tup)
    temp_str = " ".join(map(str, sent))
    grams = n_grams[length-1]
    return grams.get(temp_str, 0)

def knesser_ney(sent_tuple, glob_n):
    length = len(sent_tuple)
    term_1 = 0
    lambda_val = 0
    term_2 = 0
    d = 0.75
    if length > 1:
        num_1 = max(get_count(sent_tuple, 1, glob_n)-d, 0)
        denom_1 = get_count(sent_tuple[:-1], 0, glob_n)
        if denom_1 <= 0:
            denom_1 = 1
        term_1 = num_1/denom_1
        lambda_val = get_lambda(sent_tuple[:-1])
        term_2 = knesser_ney(sent_tuple[1:], glob_n)
        if term_1 != None and lambda_val != None and term_2 != None and (term_1 + lambda_val*term_2 > 0):
            return term_1 + lambda_val*term_2
        else:
            return(knesser_ney(sent_tuple[1:]), glob_n)
    if length == 1:
        fin_num = max(get_count(sent_tuple, 0, glob_n) - d, 0)
        fin_denom = 0
        for key_1 in uni_grams.values():
            fin_denom += key_1
        if fin_denom <=0: fin_denom=1
        lamb_term = d/fin_denom
        return ((fin_num/fin_denom) + lamb_term)


def witten_bell(sent_tuple, glob_n):
    tup_len = len(sent_tuple)
    if tup_len == 1:
        n_1 = len(set(uni_grams.keys()))
        sum = 0
        for value in uni_grams.values():
            sum += value
        d_1 = n_1 + value
        l_22 = n_1/d_1
        l_11 = 1-l_22
        num_1 = get_count(sent_tuple, 0, glob_n)
        den_1 = sum
        if num_1 == 0:
            num_1 = unk_cnt[1]
            return (num_1/den_1) * l_11
        return (num_1/den_1)
    else:
        term_1_num = get_count(sent_tuple, 0, glob_n)
        denom = get_count(sent_tuple[:-1], 0, glob_n)
        if denom <= 0:
            denom = 1
        lamb_num = get_witten(sent_tuple[:-1])
        lamb_denom = lamb_num + denom
        l_1 = 1 - (lamb_num/lamb_denom)
        l_2 = (lamb_num/lamb_denom)
        answer = (term_1_num/denom)*l_1 + l_2 * \
            (witten_bell(sent_tuple[1:], glob_n))
        if answer == 0:
            return(witten_bell(sent_tuple[1:], glob_n))
        else:
            #print("returning: ", answer)
            return answer





def get_perp_1(sent):
    #print("kn")
    input1 = sent
    input1 = tokenize(" " + input1.lower() + " ")
    temp_len = len(input1.split())
    input1 = input1.split()
    n_here = 4
    sent_prob = 1
    prod_prob = 1
    count = 1e-6
    for i in range(0, temp_len):
        if i < n_here-1:
            count += 1
            temp_tuple = tuple(input1[:i+1])
            glob_n = len(temp_tuple)
            loc_score = knesser_ney(temp_tuple, glob_n)
            sent_prob = sent_prob * loc_score
            prob_prob = prod_prob*loc_score
        else:
            count += 1
            temp_tuple = tuple(input1[i-n_here+1:i+1])
            glob_n = len(temp_tuple)
            loc_score = knesser_ney(temp_tuple, glob_n)
            sent_prob = sent_prob * loc_score
            prob_prob = prod_prob*loc_score
    if count == 0:
        count = 1
    perp_score = np.power(1/sent_prob, 1/count)
    return perp_score, sent_prob


def get_perp_2(sent):
    #print("wb")
    input1 = sent
    input1 = tokenize(" " + input1.lower() + " ")
    temp_len = len(input1.split())
    input1 = input1.split()
    n_here = 4
    sent_prob = 1
    prod_prob = 1
    count = 0
    for i in range(0, temp_len):
        if i < n_here-1:
            count += 1
            temp_tuple = tuple(input1[:i+1])
            glob_n = len(temp_tuple)
            loc_score = witten_bell(temp_tuple, glob_n)
            sent_prob = sent_prob * loc_score
            prob_prob = prod_prob*loc_score
        else:
            count += 1
            temp_tuple = tuple(input1[i-n_here+1:i+1])
            glob_n = len(temp_tuple)
            loc_score = witten_bell(temp_tuple, glob_n)
            sent_prob = sent_prob * loc_score
            prob_prob = prod_prob*loc_score
    if count == 0:
        count = 1
    perp_score = np.power(1/sent_prob, 1/count)
    return perp_score, sent_prob





file1 = open(file_n, 'r')
val_file = open("valid_1.txt", "w")
temp_str = ""
file_list = {file1}
for file in file_list:
    for line in file:
        list_words = line.split()
        for word in list_words:
            word = re.sub(r'[^\w\s!?.]', ' ', word)
            if not word.isdigit():
                temp_str += word.lower()
                temp_str += " "
            if word.isdigit():
                temp_str += "numhere"
                temp_str += " "

init_sent = re.split(r'[.!?]', temp_str)
val_data = random.sample(init_sent, k=1000)
for element in val_data:
    init_sent.remove(element)
for elem in val_data:
    print(elem, file=val_file)
temp_str = ""
for item in init_sent:
    temp_str = temp_str + item + "."
val_file.close()

fin_str = tokenize(temp_str)
fin_corpus = fin_str
test_corpus = fin_corpus


corpus_sent = re.split(r'[.!?]', fin_str)
val_data = list(random.sample(corpus_sent, k=1000))
for element in val_data:
    corpus_sent.remove(element)


extra_sym = {".", "?", ",", ";", "!", "-"}
new_corpus = ""
for char in test_corpus:
    if char in extra_sym:
        continue
    else:
        new_corpus += char

uni_lists = list()
uni_lists = new_corpus.split()
uni_grams = dict()
for word in uni_lists:
    if word in uni_grams.keys():
        uni_grams[word] += 1
    else:
        uni_grams[word] = 1


bi_grams = dict()
tri_grams = dict()
four_grams = dict()
for sent in corpus_sent:
    loc_list = sent.split()
    str_len = len(loc_list)
    for i in range(0, str_len-1):
        bi_str = ""
        bi_str = loc_list[i].strip() + " " + loc_list[i+1].strip()
        bi_str = ''.join(re.findall(r'[a-zA-Z ]', bi_str))
        # print(len(bi_str.split()))
        if len(bi_str.split()) == 2:
            if bi_str in bi_grams.keys():
                bi_grams[bi_str] += 1
            else:
                bi_grams[bi_str] = 1
    for i in range(0, str_len-2):
        tri_str = ""
        tri_str = loc_list[i].strip() + " " + loc_list[i +
                                                       1].strip() + " " + loc_list[i+2].strip()
        tri_str = ''.join(re.findall(r'[a-zA-Z ]', tri_str))
        if len(tri_str.split()) == 3:
            if tri_str in tri_grams.keys():
                tri_grams[tri_str] += 1
            else:
                tri_grams[tri_str] = 1
    for i in range(0, str_len-3):
        four_str = ""
        four_str = loc_list[i].strip() + " " + loc_list[i+1].strip() + \
            " " + loc_list[i+2].strip() + " " + loc_list[i+3].strip()
        four_str = ''.join(re.findall(r'[a-zA-Z ]', four_str))
        if len(four_str.split()) == 4:
            if four_str in four_grams.keys():
                four_grams[four_str] += 1
            else:
                four_grams[four_str] = 1


unk_cnt = dict()
unk_cnt[1] = 0
unk_cnt[2] = 0
unk_cnt[3] = 0
for item in uni_grams.keys():
    if uni_grams[item] == 1:
        unk_cnt[1] += 1
for item in bi_grams.keys():
    if bi_grams[item] == 1:
        unk_cnt[2] += 1

for item in tri_grams.keys():
    if tri_grams[item] == 1:
        unk_cnt[3] += 1


n_grams = [uni_grams, bi_grams, tri_grams, four_grams]
d = 0.75
ch = 1
if smooth_type == "k":
    ch = 1
else:
    ch = 2

input_1 = input("Enter Sentence: ")
if ch==1:
    list_ans = list()
    list_ans = get_perp_1(str(input_1))
    print("Perplexity: ", list_ans[0], "Probability: ", list_ans[1])

if ch == 2:
    list_ans = list()
    list_ans = get_perp_2(str(input_1))
    print("Perplexity: ", list_ans[0], "Probability: ", list_ans[1])
