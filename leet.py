from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import re

import numpy as np

spam = [
    "Congratulations! You have won a free vacation. Claim your prize today.",
    "Your account has been selected to receive a cash reward. Click here now.",
    "Limited time offer! Buy one get one free today.",
    "You have won a $500 gift card. Claim it before it expires.",
    "Urgent! Verify your account to receive your reward.",
    "Earn money from home with this exclusive offer.",
    "You have been selected as today's lucky winner.",
    "Click here to claim your free bonus now.",
    "Your payment was approved. Receive your cashback today.",
    "Exclusive offer just for you. Win amazing prizes now."
]

ham = [
    "Hi, are we still meeting today at 3 PM?",
    "Please review the project report before tomorrow's meeting.",
    "Your account password was updated successfully.",
    "Don't forget to bring your laptop to the office today.",
    "Can you send me the meeting notes when you have time?",
    "The payment for your order has been received. Thank you.",
    "Let's have lunch after the team meeting today.",
    "I shared the project files with you yesterday.",
    "Your package will arrive tomorrow according to the delivery schedule.",
    "Please call me when you get home safely."
]

vocabulary = set()

for message in spam + ham:
    words = re.findall(r"\b\w+\b", message.lower())  # Split into lowercase words
    vocabulary.update(words)
spamwords={}
hamwords={}
for message in spam:
    words = message.lower().replace(',','').replace('.','').replace('?','').replace('!','').split()
    for word in words:
        if word in spamwords:
            spamwords[word] +=1
        else:
            spamwords[word]= 1



for message in ham:
    words = message.lower().replace(',','').replace('.','').replace('?','').replace('!','').split()
    for word in words:
        if word in hamwords:
            hamwords[word] +=1
        else:
            hamwords[word]= 1


probability_ham = ham.__len__()/(ham.__len__()+spam.__len__())
probability_spam= 1-probability_ham
probability_of_word= probability_ham
probability_of_word_spam=probability_spam
test= 'Thank you for updating your account password.'

for word in test.lower().replace(',','').replace('.','').replace('?','').replace('!','').split():
    
    prob =hamwords[word]  if word in hamwords else 0 
    probability_of_word*=prob+1/(ham.__len__()+len(vocabulary))
        
    drop = spamwords[word]if word in spamwords else 0 
    probability_of_word_spam*=drop+1/(spam.__len__()+len(vocabulary))
    print(probability_of_word_spam)



if probability_of_word>probability_of_word_spam:
    print('its not spam')

else:
    print('its spam', probability_of_word_spam)

 