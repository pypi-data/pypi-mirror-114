#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from itertools import product


def InitSuperDiPwm(diPwm,q):
    """ Initialize the list of scores of all the q-grams of each interval of the partitionned diPwm. 

    Args:
        diP (diPWM): object diPWM

        q (int): size of the super alphabet

    Returns:
        list of tuples: a list of tuples (a, b, d) per position where d is the score of each q-grams into the interval [a,b] (the size of the interval [a,b] is q except for the last).
    """
    L = [
            (q*i,min(q*(i+1)-1, len(diPwm)-1))
            for i in range((len(diPwm)+q-1)// q)
        ]

    return [
            (a,b,{
                j : sum([
                        diPwm.value[a+i][mot[i]+mot[i+1]] for i in range(b-a+1)
                    ])
                for j,mot in enumerate(product(diPwm.alphabet, repeat=b-a+2))
            })
            for a,b in L
        ]


def search_super(diPwm, text, threshold, q):
    """ Search of the diPWM through a text by sliding window and by using a super alphabet of size q for a given threshold.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif

        threshold (float): threshold given to select the windows

        q (int): size of the super alphabet

    Yields:
        tuple: position in the text (first position = 0), sub-string, score
    """
    superDiPwm = InitSuperDiPwm(diPwm,q)

    di_alph = {
                k : v
                for v,k in enumerate(diPwm.alphabet)
            }

    list_positions = [
            [
                a,b+1,sum([
                    pow(diPwm.alphabet_size,b-a+1-i)*di_alph[x]
                for i,x in enumerate(text[a:b+2])
                ])
            ]
            for a,b,list_scores in superDiPwm
        ]

    superDiPwmLight = [x for (a,b,x) in superDiPwm]

    for j in range(len(text) - len(diPwm) - 1):
        score = 0
        for (i,(c,d,x)) in enumerate(list_positions):
            y = (x*diPwm.alphabet_size % pow(diPwm.alphabet_size,d-c+1)) + di_alph[text[d+1]]
            score += superDiPwmLight[i][y]
            list_positions[i][0] += 1
            list_positions[i][1] += 1
            list_positions[i][2] = y

        if score >= threshold:
            yield list_positions[0][0], text[list_positions[0][0]:list_positions[-1][1]+1], score
