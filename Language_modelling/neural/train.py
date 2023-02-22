import argparse
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
from model import Model
from dataset import Dataset
import re
from preprocess import tokenize


device = "cuda" if torch.cuda.is_available() else "cpu"
print("using device: ", device)

def train(dataset, model, args):
    model.train()
    dataloader = DataLoader(dataset, batch_size=args.batch_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(args.max_epochs):
        state_h, state_c = model.init_state(args.sequence_length)
        
        for batch, (x,y) in enumerate(dataloader):
            optimizer.zero_grad()
            y_pred, (state_h, state_c) = model(x,(state_h, state_c))
            loss = criterion(y_pred.transpose(1,2),y)
            state_h = state_h.detach()
            state_c = state_c.detach()
            loss.backward()
            optimizer.step()
            print({ 'epoch': epoch, 'batch': batch, 'loss': loss.item() })


def predict(dataset, model, text, next_words = 10):
    model.eval()
    #ords_r = text.split(" ")
    words = tokenize(text)[0].split()
    #words = text.split()
    state_h, state_c = model.init_state(len(words))
    for i in range(0, next_words):
        x = torch.tensor([[dataset.word_to_index.get(w,2)
                         for w in words[i:]]]).to(device)
        y_pred, (state_h, state_c) = model(x,(state_h, state_c))
        last_word_logits = y_pred[0][-1]
        p = torch.nn.functional.softmax(last_word_logits, dim=0).detach().cpu().numpy()
        word_index = np.random.choice(len(last_word_logits), p=p)
        if dataset.index_to_word[word_index] != "<unk>":
            words.append(dataset.index_to_word[word_index])
    
    return words


def get_probability(dataset, model, text):
    model.eval()
    text = " " + text + " "
    #print(tokenize(text))
    words = tokenize(text)[0].split()
    #print(words)
    for i in range(len(words)):
      if words[i] not in dataset.get_uniq_words():
        words[i] = "<unk>"
    prob = 1
    print(len(words))
    for i in range(1, len(words)):
        print(i)
        x = torch.tensor([[dataset.word_to_index[w]
                         for w in words[:i]]]).to(device)

        state_h, state_c = model.init_state(i)
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))

        last_word_logits = y_pred[0][-1]
        #print(last_word_logits)
        p = torch.nn.functional.softmax(
            last_word_logits, dim=0).cpu().detach().numpy()
        word_index = dataset.word_to_index[words[i]]
        print(dataset.index_to_word[word_index], p[word_index])
        prob *= p[word_index]
        print(p[word_index], word_index)

    return prob
        


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default = "corpus_2.txt")
parser.add_argument('--max-epochs', type=int, default=25)
parser.add_argument('--batch-size', type=int, default=128)
parser.add_argument('--sequence-length', type=int, default=4)
args = parser.parse_args()

print("ch1")
dataset = Dataset(args)
#print(dataset.uniq_words)
print("ch2")
model = Model(dataset).to(device)
print(args)
print("ch3")
train(dataset, model, args)
torch.save(model,"model_2.pth")
