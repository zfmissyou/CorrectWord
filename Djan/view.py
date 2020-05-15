from django.shortcuts import render
import re
from collections import Counter

# One character in the string gets deleted incorrectly
def RemoveOneL(word):
    splits = [ ]
    for i in range(len(word)):
        splits.append((word[:i] + word[i + 1:]))
    return (splits)

# One character in the string is incorrectly
def Replace(word):

    splits = [ ]
    for i in range(len(word)):
        for each in letters:
            splits.append(word[:i] + each + word[i + 1:])
    return (splits)

# While typing hurriedly, the user ends up swapping one pair of consecutive characters
def Exchange(word):

    splits = [ ]
    for i in range(len(word) - 1):
        splits.append((word[:i] + word[i + 1] + word[i] + word[i+2:]))
    return (splits)

letters = 'abcdefghijklmnopqrstuvwxyz'

# The user ends up inserting one extra character somewhere in the string
def Insert(word):
    splits = [ ]
    for i in range(len(word) + 1):
        for each in letters:
            splits.append(word[:i] + each + word[i:])
    return (splits)

# Collect all of condition of a word which may include a correct word
def PosblCondton(word):
    return set(RemoveOneL(word) + Exchange(word) + Replace(word) + Insert(word))

# Using Regular expressions to find all of English words and make them lower
def getcor(text):
    return re.findall(r'\w+', text.lower())

# calculate the percent of every words in all words
countwords = Counter(getcor(open('corpus-challenge5.txt', mode='r').read()))

# verify which words are correct through comparing param to corpus
def Comparing(words):
    spilt = []
    for each in words:
        if each in countwords:
            spilt.append(each)
    return set(spilt)


# contrasting and return a possible correct word
def MostPossible(word):
    # if an user enters a correct word, it will be output.
    split = Comparing([word])
    if split != set():
        return split
    # if an user enters a word that one letter be changed, it will be output.
    split2 = Comparing(PosblCondton(word))
    if (split2 != set()):
        return split2
    # if the word is not found in this corpus, it will be output
    return  [word]

#calculate sum of appearence of all words
Sumword = sum(countwords.values())

# calculate the percentage of a word in sum of appearence of all words
def Percent(word):
    return countwords[word] / Sumword

# According the percentage to choose a correct word
def judge(word):
    return (max(MostPossible(word), key=Percent))

# Get and return correct words in website and turn lower case
def data1(request):
    data = {}
    sum1 = ''
    if request.method == 'POST':
        input1 = request.POST.get('input')
        for each in input1.split():
            sum1 += judge(each.lower()) + '<br/>'
        data['data1'] = sum1
    return render(request, 'index.html', data)