import random
import pprint
import pandas
import argparse
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
from model import Model
from dataset import Dataset
import re
import math
import sys
from preprocess import tokenize
device = "cuda" if torch.cuda.is_available() else "cpu"
print("using device: ", device)


def predict(dataset, model, text, next_words=10):
    model.eval()
    #ords_r = text.split(" ")
    words = tokenize(text)[0].split()
    state_h, state_c = model.init_state(len(words))
    for i in range(0, next_words):
        x = torch.tensor([[dataset.word_to_index.get(w, 2)
                         for w in words[i:]]]).to(device)
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))
        last_word_logits = y_pred[0][-1]
        p = torch.nn.functional.softmax(
            last_word_logits, dim=0).detach().cpu().numpy()
        word_index = np.random.choice(len(last_word_logits), p=p)
        if dataset.index_to_word[word_index] != "<unk>":
            words.append(dataset.index_to_word[word_index])

    return words


def get_probability(dataset, model, text):
    model.eval()
    count = 0
    text = " " + text + " "
    words = tokenize(text)[0].split()
    prob = 1
    for i in range(1, len(words)):
        count += 1
        x = torch.tensor([[dataset.word_to_index.get(w, 2)
                         for w in words[:i]]]).to(device)

        state_h, state_c = model.init_state(i)
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))

        last_word_logits = y_pred[0][-1]
        p = torch.nn.functional.softmax(
            last_word_logits, dim=0).cpu().detach().numpy()
        word_index = dataset.word_to_index.get(words[i],2)
        prob *= p[word_index]
    list_h = [prob, count]
    return list_h


def get_perp(dataset, model, text):
    list_loc = list()
    list_loc = get_probability(dataset, model, text)
    prob_b = list_loc[0]
    count = list_loc[1] + 1
    perplexity = math.pow(1/prob_b, 1/count)
    return perplexity


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default="corpus_1.txt")
parser.add_argument('--max-epochs', type=int, default=25)
parser.add_argument('--batch-size', type=int, default=128)
parser.add_argument('--sequence-length', type=int, default=4)
args = parser.parse_args()

print("loading dataset...")
dataset = Dataset(args)
if args.dataset == "corpus_1.txt":
    print("loading model...")
    model = torch.load("model_1.pth")
else:
    print("loading model...")
    model = torch.load("model_2.pth")

input1 = input("Enter Sentence: ")
print("getting probability and perplexity...")
ans_list = list()
ans_list = get_probability(dataset, model, input1)
perp = get_perp(dataset, model, input1)
print("probability: ", ans_list[0], "perplexity: ")
