import torch
import pandas as pd
from collections import Counter
import re
import random
from preprocess import tokenize
device = "cuda" if torch.cuda.is_available() else "cpu"

class Dataset(torch.utils.data.Dataset):
    def __init__(self, args):
        self.args = args
        self.words = self.load_words(self)
        self.uniq_words = self.get_uniq_words()
        self.index_to_word = {index: word for index,
                              word in enumerate(self.uniq_words)}
        self.word_to_index = {word: index for index,
                              word in enumerate(self.uniq_words)}
        self.words_indexes = [self.word_to_index.get(w,1) for w in self.words]
        self.word_to_index["<unk>"] = 2
        self.index_to_word[2] = "<unk>"
    def load_words(self, args):

        def data_split(list_sent, t, v):
            file_v = open("val_data.txt","w")
            file_t = open("test_data.txt", "w")
            val_data = random.sample(list_sent, k=int(v*len(list_sent)))
            for item in val_data:
                list_sent.remove(item)
                print(item, file=file_v)
            test_data = random.sample(list_sent, k=int(t*len(list_sent)))
            for item in test_data:
                list_sent.remove(item)
                print(item, file = file_t)
            return list_sent

        file_1 = open(self.args.dataset)
        temp_str = ""
        for line in file_1:
            list_words = line.split()
            for word in list_words:
                word = re.sub(r'[^\w\s!?.]', ' ', word)
                if not word.isdigit():
                    temp_str += word.lower()
                    temp_str += " "
                if word.isdigit():
                    temp_str += "numhere"
                    temp_str += " "
        temp_str = temp_str.replace("_", " ")
        list_sent = tokenize(temp_str)
        list_sent = data_split(list_sent, 0.10, 0.10)
        file_m = open("train_1.txt","w")
        for item in list_sent:
            print(item, file = file_m)

        list_of_words = list()
        for sent in list_sent:
            temp_list = list(sent.split())
            list_of_words.append("<sos>")
            for i in range(0,len(temp_list)):
                list_of_words.append(temp_list[i])
            list_of_words.append("<eos>")
        word_dict = Counter(list_of_words)        
        list_of_words[1] = "<unk>"
        return list_of_words


    def get_uniq_words(self):
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)


    def __len__(self):
        return len(self.words_indexes) - self.args.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index:index+self.args.sequence_length]).to(device),
            torch.tensor(self.words_indexes[index+1:index+self.args.sequence_length+1]).to(device),
        )

