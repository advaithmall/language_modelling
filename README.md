# INLP Assignment 1
## Use this link to download model_2.pth: <a href="https://iiitaphyd-my.sharepoint.com/:u:/g/personal/advaith_malladi_research_iiit_ac_in/EdfLdWlpZVZCld9VjnEzx6QBt11gOde3Ver0_9Meh8PYKg?e=1iRGYK" target="_blank">LINK</a>  <br/><br/>


### Name: Advaith Malladi
### Roll Number: 2021114005

### Directory Structure
```
.
├── neural
│   ├── 2021114005_LM5_test-perplexity.txt
│   ├── 2021114005_LM5_train-perplexity.txt
│   ├── 2021114005_LM6_test-perplexity.txt
│   ├── 2021114005_LM6_train-perplexity.txt
│   ├── corpus_1.txt
│   ├── corpus_2.txt
│   ├── dataset.py
│   ├── model_1.pth
│   ├── model_2.pth
│   ├── model.py
│   ├── neural_language_model.py
│   ├── preprocess.py
│   └── train.py
├── ReadMe.md
├── report.pdf
└── smooth
    ├── 2021114005_LM1_test-perplexity.txt
    ├── 2021114005_LM1_train-perplexity.txt
    ├── 2021114005_LM2_test-perplexity.txt
    ├── 2021114005_LM2_train-perplexity.txt
    ├── 2021114005_LM3_test-perplexity.txt
    ├── 2021114005_LM3_train-perplexity.txt
    ├── 2021114005_LM4_test-perplexity.txt
    ├── 2021114005_LM4_train-perplexity.txt
    ├── corpus_1.txt
    ├── corpus_2.txt
    └── language_model.py

<path to corpus> = 'corpus_1.txt' (pride and prejudice) or 'corpus_2.txt' (Ulysses)


```
## To read analysis, please read report.pdf


## To run smoothing methods:
```
cd smooth

```
### once inside, RUN:

```
python3 language_model.py <smoothing type> <path to corpus>

smoothing type: k: knesser ney, w: witten bell
```
### Enter a sentence after prompt to look at the probability and perplexity of the sentence

## To run Neural Language Model

```
cd neural

```

### once inside, RUN:

```

python3 neural_language_model --dataset <path to corpus>

```
### Enter a sentence after prompt to look at the probability and perplexity of the sentence



