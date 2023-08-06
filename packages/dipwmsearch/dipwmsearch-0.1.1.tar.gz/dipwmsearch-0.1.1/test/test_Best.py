#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
from src.BestWords import get_first_threshold, count_words, find_threshold_dichotomy, find_threshold_dichotomy_optimized, find_best_words

def test_first_threshold():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    c = get_first_threshold(diPwm_matrix_new, 1000)

    assert round(c,6) == 21.663316

def test_count_words():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    c = get_first_threshold(diPwm_matrix_new, 1000)
    sol = count_words(diPwm_matrix_new, c, 2000)

    assert sol == 1

def test_find_threshold_dichotomy():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    threshold = find_threshold_dichotomy(diPwm_matrix_new, 1000, 2000)

    assert round(threshold,6) == 14.606681

def test_find_threshold_dichotomy_optimized():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    threshold = find_threshold_dichotomy_optimized(diPwm_matrix_new, 1000,2000)

    assert round(threshold,6) == 14.772161

def test_find_best_words():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    sol = find_best_words(diPwm_matrix_new,10)

    assert [(x,round(y,6)) for x,y in sol] == [('CGGTCACGTGAC', 21.667164), ('GGGTCACGTGAC', 21.577231), ('TGGTCACGTGAC', 21.507651), ('CGGTCACGTGAG', 21.415541), ('GGGTCACGTGAG', 21.325608), ('TGGTCACGTGAG', 21.256028), ('CGGTCACGTGAT', 21.239144), ('AGGTCACGTGAC', 21.226616), ('GGGTCACGTGAT', 21.149211), ('TGGTCACGTGAT', 21.079631)]
